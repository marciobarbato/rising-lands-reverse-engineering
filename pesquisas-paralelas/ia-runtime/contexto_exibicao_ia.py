"""Static display context of a binding or boundary event, from the intact executable's direct-call graph.

M2.1 found the display context of the reference events natively, by tracking display-root nesting in a
fresh run. Beyond frame 1 the native runs belong to the Mac mini, so the N-frame comparator classifies each
reference event by the routine that issued it (the owner of ``caller_return - 1``, or the routine named in a
boundary's ``caller``):

- D is the closure of the policy display roots over direct ``call imm32`` edges.
- L is the closure of the frame-phase logic roots (CalculGame, ProgIteration and the two pumps the
  ``_WinMain@16`` loop calls), cut at the display roots. Edges into a display root stay display context.
- An issuer in D - L is display context. An issuer outside D is logic context. An issuer in both D and L
  cannot be classified statically, so ``ContextoAmbiguo`` names it and its address.

Indirect calls (COM vtables, import thunks) issue their events inside the routine that holds the call, which is
exactly the issuer used here.
"""
import bisect

LOGICA = ('CalculGame', 'ProgIteration', 'PlaySnd_Manage', 'MCICD_Manage')


class ContextoAmbiguo(RuntimeError):
    def __init__(self, rotina, endereco):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: called from display roots and from logic; context of the event at '
                         f'0x{endereco:08x} needs the capture')


class ContextoExibicao:
    def __init__(self, imagem, raizes_exibicao, raizes_logica=LOGICA):
        self.imagem = imagem
        self.nomes = {n: a for a, ns in imagem.names.items() for n in ns}
        self.inicios = sorted(imagem.names)
        self.raizes = {self.nomes[r] for r in raizes_exibicao if r in self.nomes}
        self._arestas = {}
        self.exibicao = self._fecho(self.raizes, corte=set())
        self.logica = self._fecho({self.nomes[r] for r in raizes_logica if r in self.nomes}, corte=self.raizes)
        self.somente_exibicao = self.exibicao - self.logica
        self.compartilhadas = self.exibicao & self.logica

    def _chamadas(self, inicio):
        if inicio not in self._arestas:
            alvos = set()
            fim = self.imagem.symbol_end(inicio)
            for x in self.imagem.md.disasm(self.imagem.read(inicio, fim), inicio):
                if x.mnemonic == 'call' and x.op_str.startswith('0x'):
                    alvo = int(x.op_str, 16)
                    if alvo in self.imagem.names:
                        alvos.add(alvo)
            self._arestas[inicio] = alvos
        return self._arestas[inicio]

    def _fecho(self, raizes, corte):
        vistos, pilha = set(), list(raizes)
        while pilha:
            a = pilha.pop()
            if a in vistos:
                continue
            vistos.add(a)
            pilha += [b for b in self._chamadas(a) if b not in corte]
        return vistos

    def dono(self, endereco):
        i = bisect.bisect_right(self.inicios, endereco) - 1
        return self.inicios[i]

    def _classe(self, inicio, endereco):
        if inicio in self.somente_exibicao:
            return 'display'
        if inicio in self.compartilhadas:
            raise ContextoAmbiguo(self.imagem.name(inicio), endereco)
        return 'logic'

    def vinculo(self, evento):
        """'display' or 'logic' for a reference binding (``caller_return`` is the address after its call)."""
        retorno = int(evento['caller_return'], 16)
        return self._classe(self.dono(retorno - 1), retorno)

    def fronteira(self, evento):
        """'display' or 'logic' for a reference boundary, by the routine named in ``caller`` (``Name+0xoff``)."""
        nome = evento['caller'].split('+')[0]
        inicio = self.nomes[nome]
        return self._classe(inicio, int(evento['caller_return'], 16))

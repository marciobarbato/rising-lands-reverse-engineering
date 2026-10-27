// Rastreia referências e chamadores até a profundidade declarada.
// @category RisingLands
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.Reference;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class RastrearChamadores extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        Path saida = Paths.get(args[0]);
        Files.createDirectories(saida);
        int profundidade = Integer.parseInt(args[1]);
        Set<Address> fronteira = new TreeSet<>(), visitados = new TreeSet<>();
        Set<Function> funcoes = new TreeSet<>(Comparator.comparing(Function::getEntryPoint));
        List<String> arestas = new ArrayList<>();
        arestas.add("nivel\tdestino\tinstrucao_origem\tfuncao_origem\ttipo");
        for (int i=2; i<args.length; i++) fronteira.add(toAddr(Long.decode(args[i])));
        for (int nivel=0; nivel<profundidade; nivel++) {
            Set<Address> proxima = new TreeSet<>();
            for (Address destino : fronteira) {
                if (!visitados.add(destino)) continue;
                for (Reference ref : getReferencesTo(destino)) {
                    Function f = currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
                    arestas.add(nivel+"\t"+destino+"\t"+ref.getFromAddress()+"\t"+
                        (f==null?"sem_funcao":f.getEntryPoint())+"\t"+ref.getReferenceType());
                    if (f!=null) { funcoes.add(f); proxima.add(f.getEntryPoint()); }
                }
            }
            fronteira = proxima;
        }
        Files.write(saida.resolve("chamadores.tsv"),arestas,StandardCharsets.UTF_8);
        List<String> indice = new ArrayList<>();
        indice.add("endereco\tnome\ttamanho_corpo");
        for (Function f : funcoes) {
            List<String> linhas = new ArrayList<>();
            linhas.add("; SHA-256 da cópia analisada: "+currentProgram.getExecutableSHA256());
            linhas.add("; "+f.getName()+"; corpo reconhecido pelo Ghidra, pode ter limites incompletos.");
            for (Instruction ins : currentProgram.getListing().getInstructions(f.getBody(),true))
                linhas.add(ins.getAddress()+"  "+ins.toString());
            Files.write(saida.resolve(f.getEntryPoint()+".asm"),linhas,StandardCharsets.UTF_8);
            indice.add(f.getEntryPoint()+"\t"+f.getName()+"\t"+f.getBody().getNumAddresses());
        }
        Files.write(saida.resolve("funcoes.tsv"),indice,StandardCharsets.UTF_8);
        println("Rastreamento: "+funcoes.size()+" funções, "+(arestas.size()-1)+" referências.");
    }
}

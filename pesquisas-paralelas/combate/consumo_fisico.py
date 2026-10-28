"""Connect mode-1 damage to the committed shared-world physical death body."""
from consumo_dano import ConsumidorDanoUnidade
from morte_dano import MorteDanoUnidade


def criar_consumidor_fisico(mundo, pool, danos, consulta=None, efeito=None,
                            bonus_4965ac=0, mortes_sem_experiencia=False):
    """Return an opt-in consumer over writable views of mundo.unidades.

    The world owns physical state and iniciar_morte_unidade. The caller owns
    loaded damage/query/effect state and the projectile pool. Only the lethal
    SetDyingEngin request is resolved here. Level, message, sound and sympathy
    still delegate or fail at their original request; no rollback or entry
    retry follows a provider exception. Do not replace/resize backing pools or
    replace records during callbacks. Views retain the original backing pool.
    mortes_sem_experiencia explicitly enables the separate mode-3/4 common
    lethal tail; its default False and the mode-8/9 stops are unchanged.
    """
    if not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800:
        raise ValueError('Expected the writable 800-record Core unit pool')
    if not callable(getattr(mundo, 'iniciar_morte_unidade', None)):
        raise ValueError('Expected the Core physical death provider')
    units = memoryview(mundo.unidades)
    records = tuple(units[i:i+276] for i in range(0, 220800, 276))

    def lethal_effect(name, args):
        if name == 'SetDyingEngin':
            return mundo.iniciar_morte_unidade(*args)
        if efeito is None:
            raise NotImplementedError('External lethal effect required: ' + name)
        return efeito(name, args)

    death = MorteDanoUnidade(records, pool, lethal_effect)
    return ConsumidorDanoUnidade(records, danos, consulta, efeito,
        jogador_local=mundo.jogador_local, bonus_4965ac=bonus_4965ac, morte=death,
        morte_sem_experiencia=death.sem_experiencia if mortes_sem_experiencia else None)

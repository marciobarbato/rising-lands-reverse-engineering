// Aplica apenas campos e assinaturas sustentados pela inspeção do assembly.
// @category RisingLands
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.data.*;
import ghidra.program.model.symbol.SourceType;

public class AnotarUnidades extends GhidraScript {
    private void campo(StructureDataType estrutura, int offset, DataType tipo, String nome, String evidencia) {
        estrutura.replaceAtOffset(offset, tipo, tipo.getLength(), nome, evidencia);
    }
    private void getter(long endereco, String nome, DataType retorno, String registrador) throws Exception {
        Function f = getFunctionAt(toAddr(endereco));
        if (f == null) { disassemble(toAddr(endereco)); f = createFunction(toAddr(endereco), nome); }
        if (f == null) throw new IllegalStateException("Função ausente: "+Long.toHexString(endereco));
        f.setName(nome, SourceType.USER_DEFINED);
        f.setCallingConvention(Function.UNKNOWN_CALLING_CONVENTION_STRING);
        f.setCustomVariableStorage(true);
        f.replaceParameters(Function.FunctionUpdateType.CUSTOM_STORAGE, true, SourceType.USER_DEFINED,
            new ParameterImpl("indice_unidade", UnsignedShortDataType.dataType,
                              currentProgram.getRegister("AX"), currentProgram));
        f.setReturn(retorno, new VariableStorage(currentProgram, currentProgram.getRegister(registrador)), SourceType.USER_DEFINED);
        f.setStackPurgeSize(0);
        f.setComment("Assinatura recuperada: índice em AX, resultado em "+registrador+". Convenção interna por registradores; não presumir stdcall/fastcall.");
    }
    public void run() throws Exception {
        DataType u8 = ByteDataType.dataType, u16 = UnsignedShortDataType.dataType;
        StructureDataType unidade = new StructureDataType(new CategoryPath("/RisingLands"), "UnidadeParcial", 0x114);
        campo(unidade,0,u8,"proprietario_id","0x442045 lê; 0x410c16 compara com jogador local 0x508041.");
        campo(unidade,1,u8,"tipo_id","0x442025; índice de 26 tipos.");
        campo(unidade,2,u8,"estado","0x441fff: ativo se !=0; outros predicados excluem também estado 4.");
        campo(unidade,8,u16,"celula_atual","0x4421bf: x=valor%256, y=valor/256; 0x43eb64 consulta ocupação.");
        campo(unidade,0xa,u16,"campo_0a","Ainda sem semântica completa; não presumir ordem atual.");
        campo(unidade,0xc,u16,"campo_0c","Ainda sem semântica completa.");
        campo(unidade,0x7c,u16,"celula_passo","Posição comparada à atual em 0x444938; papel refinado no movimento.");
        campo(unidade,0x7e,u16,"celula_destino","0x44930c passa ao buscador de caminho 0x43b30b.");
        campo(unidade,0x86,SignedByteDataType.dataType,"deslocamento_x","Hipótese: deslocamento interpolado; confirmar no desenho.");
        campo(unidade,0x87,SignedByteDataType.dataType,"deslocamento_y","Hipótese: deslocamento interpolado; confirmar no desenho.");
        campo(unidade,0x88,u8,"estado_caminho","Switch de 0x44930c: 0,1,3,4,5,6.");
        campo(unidade,0x90,u8,"direcao_desejada","0x477042 fornece direções ímpares 1..15.");
        campo(unidade,0x91,u8,"orientacao_atual","0x448599 gira num círculo de 16 orientações.");
        campo(unidade,0x92,u8,"contador_giro","Incremento uint8 e comparação por igualdade em 0x448599.");
        campo(unidade,0x93,u8,"periodo_giro","Definido por tipo em 0x457350; não converter para segundos.");
        campo(unidade,0x97,u8,"progresso_passo","0x44889f: chegou quando maior que 31.");
        campo(unidade,0x98,u8,"incremento_passo","0x448704 soma a cada chamada, descontando DL.");
        campo(unidade,0xa4,u8,"quadro_movimento","0x449023 incrementa módulo quantidade.");
        campo(unidade,0xa5,u8,"quantidade_quadros_movimento","Inicializador 0x457350, consumidor 0x44902e.");
        campo(unidade,0xa7,u8,"periodo_animacao","0x449013 compara com contador 0xa9.");
        campo(unidade,0xa9,u8,"contador_animacao","0x448f50 incrementa e zera no período.");
        campo(unidade,0x9a,u16,"vida","0x457122 soma e limita; 0x452e8b subtrai 20 e chama morte no esgotamento.");
        campo(unidade,0xb0,u8,"alcance_quadrado_u8","0x46ae0e copia AL da tabela de tipos; truncamento adicional.");
        campo(unidade,0xbb,u8,"raio_visao","0x46ade5 copia da tabela de tipos.");
        campo(unidade,0xbc,u8,"grupo_id","Getter/setter e seleção por grupo em 0x442139.");
        campo(unidade,0xbd,u8,"selecionada","Hipótese apoiada em 0x472648 e 0x47268b.");
        campo(unidade,0x102,u16,"contador_recarga","0x46af50 copia RECHARGE.");
        DataType registrado = currentProgram.getDataTypeManager().addDataType(unidade, DataTypeConflictHandler.REPLACE_HANDLER);
        Address global = toAddr(0x4e19a0L);
        clearListing(global, global.add(3));
        createData(global, new PointerDataType(registrado, 4, currentProgram.getDataTypeManager()));
        createLabel(global,"tabela_unidades",true);
        getter(0x441fffL,"unidade_esta_ativa",BooleanDataType.dataType,"AL");
        getter(0x442025L,"unidade_obter_tipo",u8,"AL");
        getter(0x442045L,"unidade_obter_proprietario",u8,"AL");
        getter(0x442064L,"unidade_obter_campo_0c",u16,"AX");
        getter(0x442085L,"unidade_obter_campo_0a",u16,"AX");
        getter(0x4420a6L,"unidade_vida_diferente_do_maximo",BooleanDataType.dataType,"AL");
        getter(0x45718aL,"unidade_obter_vida",u16,"AX");
        println("Estrutura parcial de 276 bytes e sete assinaturas por registradores aplicadas.");
    }
}

// Exporta evidências estáticas das rotinas que acessam a tabela de unidades.
// @category RisingLands
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.io.*;

public class ExportarUnidades extends GhidraScript {
    public void run() throws Exception {
        Path saida = Paths.get(getScriptArgs()[0]).toAbsolutePath();
        Files.createDirectories(saida);
        FunctionManager fm = currentProgram.getFunctionManager();
        Map<Long, String> nomes = new LinkedHashMap<>();
        nomes.put(0x441fffL, "unidade_esta_ativa");
        nomes.put(0x442025L, "unidade_obter_tipo");
        nomes.put(0x442045L, "unidade_obter_proprietario");
        nomes.put(0x442064L, "unidade_obter_campo_0c");
        nomes.put(0x442085L, "unidade_obter_campo_0a");
        nomes.put(0x4420a6L, "unidade_vida_diferente_do_maximo");
        nomes.put(0x45718aL, "unidade_obter_vida");
        nomes.put(0x46acbfL, "carregar_unidades_eta");
        nomes.put(0x44188bL, "carregar_atributos_tipos");
        Set<Function> selecionadas = new TreeSet<>(Comparator.comparing(Function::getEntryPoint));
        for (Map.Entry<Long,String> entrada : nomes.entrySet()) {
            Address endereco = toAddr(entrada.getKey());
            Function funcao = fm.getFunctionAt(endereco);
            if (funcao == null) {
                disassemble(endereco);
                funcao = createFunction(endereco, entrada.getValue());
            }
            if (funcao != null) {
                funcao.setName(entrada.getValue(), SourceType.USER_DEFINED);
                selecionadas.add(funcao);
                for (Reference ref : getReferencesTo(endereco)) {
                    Function chamadora = fm.getFunctionContaining(ref.getFromAddress());
                    if (chamadora != null) selecionadas.add(chamadora);
                }
            }
        }
        ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(toAddr(0x4e19a0L));
        List<String> referencias = new ArrayList<>();
        referencias.add("instrucao\tfuncao\ttipo_referencia");
        while (refs.hasNext()) {
            Reference ref = refs.next();
            Function f = fm.getFunctionContaining(ref.getFromAddress());
            referencias.add(ref.getFromAddress() + "\t" + (f == null ? "sem_funcao" : f.getEntryPoint()) + "\t" + ref.getReferenceType());
            if (f != null) selecionadas.add(f);
        }
        Files.write(saida.resolve("referencias_tabela_unidades.tsv"), referencias, StandardCharsets.UTF_8);
        List<String> todas = new ArrayList<>();
        todas.add("endereco\tnome\ttamanho_corpo\tconvencao");
        for (Function f : fm.getFunctions(true)) {
            todas.add(f.getEntryPoint()+"\t"+f.getName()+"\t"+f.getBody().getNumAddresses()+"\t"+f.getCallingConventionName());
        }
        Files.write(saida.resolve("funcoes.tsv"), todas, StandardCharsets.UTF_8);
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);
        List<String> estado = new ArrayList<>();
        estado.add("endereco\tnome\tresultado");
        int numero = 0;
        for (Function f : selecionadas) {
            monitor.checkCancelled();
            DecompileResults resultado = decomp.decompileFunction(f, 20, monitor);
            String nomeArquivo = f.getEntryPoint().toString();
            String cabecalho = "/* Pseudocódigo Ghidra, não é fonte original.\n" +
                " * Função " + f.getName() + ", entrada " + f.getEntryPoint() + ".\n" +
                " * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.\n" +
                " * SHA-256: " + currentProgram.getExecutableSHA256() + "\n */\n";
            String codigo = resultado.decompileCompleted() ? resultado.getDecompiledFunction().getC() : "/* Falhou: " + resultado.getErrorMessage() + " */\n";
            Files.writeString(saida.resolve(nomeArquivo+".c"), (cabecalho+codigo).replaceAll("(?m)[ \\t]+$", "").stripTrailing()+"\n", StandardCharsets.UTF_8);
            List<String> asm = new ArrayList<>();
            for (Instruction ins : currentProgram.getListing().getInstructions(f.getBody(), true)) {
                asm.add(ins.getAddress()+"  "+ins.toString());
            }
            Files.write(saida.resolve(nomeArquivo+".asm"), asm, StandardCharsets.UTF_8);
            estado.add(f.getEntryPoint()+"\t"+f.getName()+"\t"+(resultado.decompileCompleted()?"OK":resultado.getErrorMessage().replace('\n',' ')));
            if (++numero % 50 == 0) println("Exportadas "+numero+" de "+selecionadas.size()+" rotinas");
        }
        decomp.dispose();
        Files.write(saida.resolve("exportacao.tsv"), estado, StandardCharsets.UTF_8);
        Files.writeString(saida.resolve("ambiente.txt"),
            "Ghidra: "+getGhidraVersion()+"\nLinguagem: "+currentProgram.getLanguageID()+
            "\nCompilerSpec: "+currentProgram.getCompilerSpec().getCompilerSpecID()+
            "\nSHA-256: "+currentProgram.getExecutableSHA256()+"\nFunções exportadas: "+numero+"\n", StandardCharsets.UTF_8);
        println("Exportação concluída: "+numero+" rotinas.");
    }
}

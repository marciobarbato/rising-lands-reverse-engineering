// Acrescenta rótulos franceses do SBL num namespace separado, sem renomear análises.
// @category RisingLands
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class ImportarSimbolosOriginais extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) throw new IllegalArgumentException("TSV e relatório obrigatórios");
        String hash = currentProgram.getExecutableSHA256();
        if (!hash.equals("26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0"))
            throw new IllegalArgumentException("Programa diferente da cópia normalizada identificada");
        SymbolTable tabela = currentProgram.getSymbolTable();
        Namespace ns = tabela.getNamespace("OriginaisSBL", currentProgram.getGlobalNamespace());
        if (ns == null) ns = tabela.createNameSpace(currentProgram.getGlobalNamespace(), "OriginaisSBL", SourceType.USER_DEFINED);
        List<String> resultado = new ArrayList<>();
        resultado.add("endereco\tnome_original\tresultado");
        List<String> linhas = Files.readAllLines(Paths.get(args[0]), StandardCharsets.UTF_8);
        for (String linha : linhas.subList(1, linhas.size())) {
            String[] campos = linha.split("\t", 2);
            Address a = toAddr(Long.parseLong(campos[0], 16));
            String nome = campos[1];
            if (!currentProgram.getMemory().contains(a)) throw new IllegalArgumentException("Símbolo fora da memória: " + linha);
            if (tabela.getSymbol(nome, a, ns) == null) tabela.createLabel(a, nome, ns, SourceType.USER_DEFINED);
            resultado.add(campos[0]+"\t"+nome+"\tROTULO");
        }
        for (int i=2; i<args.length; i++) {
            Address a=toAddr(Long.decode(args[i]));
            if (getFunctionAt(a)==null) {
                disassemble(a);
                if (createFunction(a, null)==null) throw new IllegalStateException("Não criou função: "+a);
            }
        }
        Files.write(Paths.get(args[1]), resultado, StandardCharsets.UTF_8);
        println("Símbolos originais importados: "+(resultado.size()-1));
    }
}

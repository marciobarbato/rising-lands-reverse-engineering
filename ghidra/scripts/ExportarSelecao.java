// Exporta uma seleção explícita; não altera nomes nem assinaturas.
// @category RisingLands
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class ExportarSelecao extends GhidraScript {
    public void run() throws Exception {
        String[] args=getScriptArgs();
        Path saida=Paths.get(args[0]); Files.createDirectories(saida);
        DecompInterface decomp=new DecompInterface(); decomp.openProgram(currentProgram);
        List<String> indice=new ArrayList<>(); indice.add("entrada\tnome\tresultado");
        for(int i=1;i<args.length;i++) {
            Function f=getFunctionAt(toAddr(Long.decode(args[i])));
            if(f==null) throw new IllegalArgumentException("Função ausente: "+args[i]);
            String hash=currentProgram.getExecutableSHA256();
            List<String> asm=new ArrayList<>(); asm.add("; SHA-256 da cópia normalizada: "+hash);
            for(Instruction ins:currentProgram.getListing().getInstructions(f.getBody(),true))
                asm.add(ins.getAddress()+"  "+ins.toString());
            Files.write(saida.resolve(f.getEntryPoint()+".asm"),asm,StandardCharsets.UTF_8);
            DecompileResults r=decomp.decompileFunction(f,30,monitor);
            if(!r.decompileCompleted()) throw new IllegalStateException(r.getErrorMessage());
            String c="/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.\n"+
                     " * SHA-256: "+hash+"\n */\n"+r.getDecompiledFunction().getC();
            Files.writeString(saida.resolve(f.getEntryPoint()+".c"),c.replaceAll("(?m)[ \\t]+$","").stripTrailing()+"\n");
            indice.add(f.getEntryPoint()+"\t"+f.getName()+"\tOK");
        }
        decomp.dispose(); Files.write(saida.resolve("exportacao.tsv"),indice,StandardCharsets.UTF_8);
        println("Seleção exportada: "+(indice.size()-1)+" funções.");
    }
}

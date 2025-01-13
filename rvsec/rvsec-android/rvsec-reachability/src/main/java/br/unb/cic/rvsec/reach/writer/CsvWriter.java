package br.unb.cic.rvsec.reach.writer;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Set;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import br.unb.cic.rvsec.reach.model.RvsecClass;
import br.unb.cic.rvsec.reach.model.RvsecMethod;

public class CsvWriter implements Writer {
    private static final Logger log = LoggerFactory.getLogger(CsvWriter.class);

    @Override
    public void write(Set<RvsecClass> result, File out) {
        log.info("Saving results in: "+out.getAbsolutePath());
        try (PrintWriter pw = new PrintWriter(new FileWriter(out))) {
            pw.println("className,isActivity,isMainActivity,methodName,reachable,reachesMop,directlyReachesMop,signature");
            for (RvsecClass clazz : result) {
                for (RvsecMethod method : clazz.getMethods()) {
                    pw.println(String.format("%s,%b,%b,%s,%b,%b,%b,\"%s\"",
                            clazz.getClassName(),
                            clazz.isActivity(),
                            clazz.isMainActivity(),
                            method.getMethodName(),
                            method.isReachable(),
                            method.isReachesMop(),
                            method.isDirectlyReachesMop(),
                            method.getMethodSignature()));
                }
            }
        } catch (IOException e) {
        	log.error("Error writing csv file: "+e.getMessage());
            throw new RuntimeException(e);
        }
    }

}

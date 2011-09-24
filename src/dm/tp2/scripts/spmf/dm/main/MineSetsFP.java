package dm.main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import ca.pfv.spmf.frequentpatterns.fpgrowth.AlgoFPGrowth;
import ca.pfv.spmf.frequentpatterns.fpgrowth.Database;
import ca.pfv.spmf.frequentpatterns.fpgrowth.Itemset;
import ca.pfv.spmf.frequentpatterns.fpgrowth.Itemsets;

/**
 * Simple script like class to run the FPGrowth algorithm. 
 * 
 * @author Flavio Figueiredo
 */
public class MineSetsFP {
	
    public static void main(String[] args) throws Exception {
        
        if (args == null || args.length < 3) {
            System.err.println("Usage java " + MineSetsFP.class +
                    " <set-file> <vocabulary-file> " + 
                    "<min-support [0,1]>");
            System.exit(1);
        }

        //Parameters
        String setFilePath = args[0];
        String vocabularyFilePath = args[1];
        double minSupport = Double.parseDouble(args[2]);

        //Loading vocabulary
        Map<Integer, String> vocabulary = new HashMap<Integer, String>();
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(
                    new FileReader(new File(vocabularyFilePath)));
            
            String line;
            while ((line = reader.readLine()) != null) {
                String[] split = line.split("\\s+");
                assert split.length == 2;
                
                int termID = Integer.parseInt(split[0]);
                String term = split[1];
                vocabulary.put(termID, term);
            }
            
        } finally {
            if (reader != null) {
                reader.close();
            }
        }
        
        //Running Algorithm
        Database context = new Database();
        context.loadFile(setFilePath);
        AlgoFPGrowth algo = new AlgoFPGrowth();
        Itemsets frequents = algo.runAlgorithm(context, minSupport);
        
        //Summarizing
        List<List<Itemset>> levels = frequents.getLevels();
        for (List<Itemset> level : levels) {
            for (Itemset iSet : level) {
                Collection<Integer> items = iSet.getItems();
                double supp = iSet.getRelativeSupport(context.size());
                
                for (Integer iid : items) {
                    System.out.print(vocabulary.get(iid) + " ");
                }
                System.out.println("-> " + supp);
            }
        }
    }
}

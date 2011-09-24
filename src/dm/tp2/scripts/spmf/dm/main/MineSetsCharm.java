package dm.main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import ca.pfv.spmf.frequentpatterns.eclat_and_charm.AlgoCharm;
import ca.pfv.spmf.frequentpatterns.eclat_and_charm.Context;
import ca.pfv.spmf.frequentpatterns.eclat_and_charm.Itemset;
import ca.pfv.spmf.frequentpatterns.eclat_and_charm.Itemsets;

/**
 * Simple script like class to run the Charm algorithm. 
 * 
 * @author Flavio Figueiredo
 */
public class MineSetsCharm {
	
    /**
     * Used to create a large hashtable
     */
    private static final int HASHTABLE_SIZE = 100000;

    public static void main(String[] args) throws Exception {
        
        if (args == null || args.length < 3) {
            System.err.println("Usage java " + MineSetsCharm.class +
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
        Context context = new Context();
        context.loadFile(setFilePath);
        AlgoCharm algo = new AlgoCharm(context, HASHTABLE_SIZE);
        Itemsets frequents = algo.runAlgorithm(minSupport, true);
        
        //Summarizing
        List<List<Itemset>> levels = frequents.getLevels();
        for (List<Itemset> level : levels) {
            for (Itemset iSet : level) {
                Set<Integer> items = iSet.getItems();
                double supp = iSet.getRelativeSupport(context.size());
                
                for (Integer iid : items) {
                    System.out.print(vocabulary.get(iid) + " ");
                }
                System.out.println("-> " + supp);
            }
        }
    }
}

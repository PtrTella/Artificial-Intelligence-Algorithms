import java.util.*;

public class Inference {

    public static void main(String[] args) {
        List<Clause> clauses = new ArrayList<>();
        // Initialize the set of clauses S
        
        // Apply resolution inference to the set of clauses S
        Set<Clause> resolvents = resolutionInference(clauses);
        
        // Print the set of resolvents
        System.out.println("Set of Resolvents: " + resolvents);
    }
    
    public static Set<Clause> resolutionInference(List<Clause> clauses) {
        Set<Clause> resolvents = new HashSet<>();
        while (true) {
            // Select two arbitrary clauses from S or any previously calculated resolvent
            Clause c1 = selectClause(clauses, resolvents);
            Clause c2 = selectClause(clauses, resolvents);
            
            // Calculate the resolvent of c1 and c2
            Clause resolvent = resolve(c1, c2);
            
            // If the resolvent is empty, the set of clauses is unsatisfiable
            if (resolvent.isEmpty()) {
                System.out.println("Unsatisfiable");
                return resolvents;
            }
            
            // If the resolvent is not already in the set of clauses or resolvents, add it
            if (!clauses.contains(resolvent) && !resolvents.contains(resolvent)) {
                resolvents.add(resolvent);
            }
            
            // If no new resolvent can be derived, return the set of resolvents
            if (resolvents.size() == clauses.size()) {
                return resolvents;
            }
        }
    }
    
    public static Clause selectClause(List<Clause> clauses, Set<Clause> resolvents) {
        // Select an arbitrary clause from S or any previously calculated resolvent
        List<Clause> candidates = new ArrayList<>(clauses);
        candidates.addAll(resolvents);
        int index = (int) (Math.random() * candidates.size());
        return candidates.get(index);
    }
    
    public static Clause resolve(Clause c1, Clause c2) {
        // Calculate the resolvent of c1 and c2
        Clause resolvent = new Clause();
        for (Literal l1 : c1.getLiterals()) {
            for (Literal l2 : c2.getLiterals()) {
                if (l1.negate().equals(l2)) {
                    Clause clause = new Clause();
                    for (Literal l : c1.getLiterals()) {
                        if (!l.equals(l1)) {
                            clause.addLiteral(l);
                        }
                    }
                    for (Literal l : c2.getLiterals()) {
                        if (!l.equals(l2)) {
                            clause.addLiteral(l);
                        }
                    }
                    resolvent = Clause.union(resolvent, clause);
                }
            }
        }
        return resolvent;
    }
}


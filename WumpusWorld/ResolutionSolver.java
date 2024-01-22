import java.util.ArrayList;
import java.util.List;

public class ResolutionSolver {

    private List<Clause> KB = new ArrayList<>();

    public static void main(String[] args) {

        
        // KB = {¬sun ∨ ¬money ∨ ice, ¬money ∨ ice ∨ movie, ¬movie ∨ money, ¬movie ∨ ¬ice,   
        //       movie V sun V money V cry}
        Clause A = new Clause(new Literal(false, "sun"), new Literal(false, "money"), new Literal(true, "ice"));
        Clause B = new Clause(new Literal(false, "money"), new Literal(true, "ice"), new Literal(true, "movie"));
        Clause C = new Clause(new Literal(false, "movie"), new Literal(true, "money"));
        Clause D = new Clause(new Literal(false, "movie"), new Literal(false, "ice"));
        Clause E = new Clause(new Literal(true, "sun"), new Literal(true, "money"), new Literal(true, "cry"));

        // Clause to prove by adding it to KB = {movie}
        Clause PROVE = new Clause(new Literal(true, "movie"));

        
        
        List<Clause> KB = new ArrayList<>();
        KB.addAll(List.of(A,B, C, D, E, PROVE));
        ResolutionSolver solver = new ResolutionSolver(KB);

        System.out.println("Input KB: " + KB + "\n");
        List<Clause> sol = solver.solver();
        System.out.println("\nSolution: " + sol);
    }

    public ResolutionSolver(List<Clause> KB) {
        this.KB.addAll(KB);
    }
    
    /**
     * Resolves two clauses in CNF.
     *
     * @param A The first clause.
     * @param B The second clause.
     * @return The resolvent of the two clauses.
     */
    public Clause resolution(Clause A, Clause B) {

        List<Literal> matchinList = new ArrayList<>();
        matchinList = A.getNegatedMatching(B);

        // Check if the clauses are contradictory.
        if (matchinList.size() != 1) {
            return null;
        }
    
        // Pick random form matching list
        // Not usefull in this case because we have only one literal in the list, And it has to be like that.
        Literal a = matchinList.get(0);

        // Create the resolvent.
        Clause resolvent = new Clause();
        resolvent.addAll(A.getLiterals());
        resolvent.addAll(B.getLiterals());
        
        // Remove the literals that match.
        resolvent.remove(a);
        resolvent.remove(a.getNegation());
    

        // Remove duplicates from the resolvent.
        resolvent.removeDuplicates();

        return resolvent;
    }

    
    /**
     * Applies the resolution mechanism to a given set of clauses.
     *
     * @param clauses The set of clauses.
     * @return A list of the resolvents of the clauses.
     */
    public  List<Clause> solver() {

        // check not redaundancy in KB
        System.out.println("CHECK REDAUNDANCY");
        List<Clause> removable = new ArrayList<>();
        for (Clause Cl1 : KB) {
            for (Clause Cl2 : KB) {
                if(KB.indexOf(Cl1) != KB.indexOf(Cl2)){
                    if (Cl1.isLowerOrEqual(Cl2)) {
                        removable.add(Cl2);
                    }
                }
            }
        }
        KB.removeAll(removable);

        
        System.out.println("KB: " + KB);
        // Initialize the list of resolvents.
        List<Clause> KBf = new ArrayList<>();
        List<Clause> S = new ArrayList<>();


        
        do {
            //System.out.println("Iteration: " + i++);
            // Set the previous KB.
            KBf = KB;
            // Clear the resolvents.
            S.clear();

            // Loop through al l the clauses.
            for (Clause A : KB) {
                for (Clause B : KB) {
                    //System.out.println("A: " + A + " B: " + B);
                    
                    // Check if the clauses are the same.
                    if (KB.indexOf(A) < KB.indexOf(B)){
                        // Resolve the clauses.
                        Clause C = resolution(A, B);
                        //System.out.println("C: " + C);
                        // Check if the resolvent is null.
                        if (C != null) {
                            S.add(C);
                        }
                    }
                }
            }

            System.out.println("S: " + S);
            
            // Check if the resolvent is empty.
            if (S.isEmpty()) {
                return KB;
            }
            
            // Incorporate the resolvents into the KB.
            for (Clause D : S) {
                KB = incorporate(KB, D);
            }
            System.out.println("KB: " + KB);

        } while(KB == KBf);

        return KB;

    }

    /**
     * Incorporates a clause into a set of clauses.
     *
     * @param KB The set of clauses.
     * @param C The clause to be incorporated.
     * @return The set of clauses with the new clause incorporated.
     */
    public static List<Clause> incorporate(List<Clause> KB, Clause A) {
        
        for (Clause B : KB) {
            // Check if the clauses are the same.
            if (B.isLowerOrEqual(A)) {
                return KB;
            }
        }

        List<Clause> removable = new ArrayList<>();

        for (Clause B : KB) {
            // Check if the clauses are the same.
            if (A.isLowerOrEqual(B)) {
                removable.add(B);
            }
        }

        KB.removeAll(removable);
        KB.add(A);
        
        return KB;
    }
}

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ResolutionSolver {

    public static void main(String[] args) {

        // KB = {¬sun ∨ ¬money ∨ ice, ¬money ∨ ice ∨ movie, ¬movie ∨ money, ¬movie ∨ ¬ice,   
        //       movie V sun V money V cry}
        Clause A = new Clause(new Literal(false, "sun"), new Literal(false, "money"), new Literal(true, "ice"));
        Clause B = new Clause(new Literal(false, "money"), new Literal(true, "ice"), new Literal(true, "movie"));
        Clause C = new Clause(new Literal(false, "movie"), new Literal(true, "money"));
        Clause D = new Clause(new Literal(false, "movie"), new Literal(false, "ice"));
        Clause E = new Clause(new Literal(true, "movie"), new Literal(true, "sun"), new Literal(true, "money"), new Literal(true, "cry"));

        // KB = {¬movie}
        Clause PROVE = new Clause(new Literal(false, "ice"));
        Clause PROVE2 = new Clause(new Literal(true, "movie"));

        System.out.println("A: " + A);
        Clause resolvent = resolution(A, A);
        System.out.println("A" + A);
        System.out.println("Resolution: " + resolvent);
        List<Clause> KB = new ArrayList<>();
        KB.addAll(List.of(A, B, C, D, E, PROVE));
        List<Clause> sol = solver(KB);
        System.out.println("Solver: " + sol);
    }
    
    /**
     * Resolves two clauses in CNF.
     *
     * @param A The first clause.
     * @param B The second clause.
     * @return The resolvent of the two clauses.
     */
    public static Clause resolution(Clause A, Clause B) {

        List<Literal> matchinList = new ArrayList<>();
        matchinList = A.getNegatedMatching(B);

        // Check if the clauses are contradictory.
        if (matchinList.size() != 1) {
            return null;
        }
    
        // Pick random form matching list
        Random ran = new Random();
        Literal a = matchinList.get(ran.nextInt(matchinList.size()));

        Clause Acopy = new Clause(A.getLiterals());
        Clause Bcopy = new Clause(B.getLiterals());

        Acopy.removeLiteral(a);
        Bcopy.removeLiteral(a.getNegation());


        // Create the resolvent.
        Clause resolvent = new Clause(Acopy, Bcopy);
    

        // Remove duplicates from the resolvent.
        resolvent.removeDuplicates();
        resolvent.getPositiveLiterals().removeIf(n -> resolvent.getNegativeLiterals().contains(n));

        return resolvent;
    }

    
    /**
     * Applies the resolution mechanism to a given set of clauses.
     *
     * @param clauses The set of clauses.
     * @return A list of the resolvents of the clauses.
     */
    public static List<Clause> solver(List<Clause> KB) {
        
        System.out.println("SOLVER" + KB);
        // Initialize the list of resolvents.
        List<Clause> KBf = new ArrayList<>();
        List<Clause> S = new ArrayList<>();
        int i = 0;
        
        do {
            //System.out.println("Iteration: " + i++);
            // Set the previous KB.
            KBf = KB;
            // Clear the resolvents.
            S.clear();

            // Loop through al l the clauses.
            for (Clause A : KB) {
                System.out.println("-------------------");
                for (Clause B : KB) {
                    System.out.println("A: " + A + "B: " + B);
                    
                    // Check if the clauses are the same.
                    if (!A.equals(B)) {
                        // Resolve the clauses.
                        Clause C = resolution(A, B);
                        // Check if the resolvent is null.
                        if (C != null) {
                            S.add(C);
                        }
                    }
                }
            }

            //System.out.println("S: " + S);
            
            // Check if the resolvent is empty.
            if (S.isEmpty()) {
                System.out.println("Empty");
                return KB;
            }
            
            // Incorporate the resolvents into the KB.
            for (Clause D : S) {
                KB = incorporate(KB, D);
            }

        } while (KB == KBf);

        System.out.println("SOLVER");
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

        for (Clause B : KB) {
            // Check if the clauses are the same.
            if (A.isLowerOrEqual(B)) {
                System.out.println("Remove: " + B + "From: " + KB);

                KB.remove(B);
                System.out.println("Remove: " + KB);
            }
        }

        KB.add(A);
        return KB;
    }
}

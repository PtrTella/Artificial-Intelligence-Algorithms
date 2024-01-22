import java.util.ArrayList;
import java.util.List;

public class Puzzles {

    public List<Clause> KB = new ArrayList<>();

    public static void main(String[] args) {
        
        Puzzles puzzles = new Puzzles();
        puzzles.KB = puzzles.RobbeyPuzzle();

        System.out.println("Input KB: " + puzzles.KB + "\n");
        ResolutionSolver solver = new ResolutionSolver(puzzles.KB);
        List<Clause> sol = solver.solver();
        System.out.println("\nSolution: " + sol);
    }

    public List<Clause> RobbeyPuzzle(){
        
        List<Clause> KB = new ArrayList<>();

        // TRUE -> is guilty, FALSE -> is innocent

        // 1. Nobody else could have been involved other than A, B and C. So: A v B v C
        Clause Cl1 = new Clause(new Literal(true, "A"), new Literal(true, "B"), new Literal(true, "C"));

        // 2. C never commits a crime without A’s participation.
        Clause Cl2 = new Clause(new Literal(false, "C"), new Literal(true, "A"));

        // 3. B does not know how to drive. So: b -> (a | c) so: (-b V a V c)
        Clause Cl3 = new Clause(new Literal(false, "B"), new Literal(true, "A"), new Literal(true, "C"));

        // SOLUTION
        KB.addAll(List.of(Cl1, Cl2, Cl3));
        return KB;
        // NOT SOLUTION for A innocent so A is guilty
    }

    public List<Clause> HatColorPuzzle(){
        /*  Three people are in a room wearing hats. Two
            of them are wearing blue hats and one of them
            is wearing a red hat. They can’t see what color
            hat they are wearing, but they can see everyone
            else’s hats. They are playing a game where their
            objective is to figure out the color of their own hat.
            If a player sees that the other two players have a red hat and a blue hat, what color hat is the
            player wearing? 
        */
        List<Clause> KB = new ArrayList<>();

        return KB;

        
        // P1 ≠ P2 ∧ P1 ≠ P3 ∧ P2 ≠ P3

    }


    public List<Clause> SKKPuzzle(){
        // (Alex = Knight) ∨ (Alex = Knave) ∨ (Alex = Spy)
        Clause Cl1 = new Clause(new Literal(true, "Alex"), new Literal(true, "Knave"), new Literal(false, "Knight"), new Literal(false, "Spy"));
        Clause Cl2 =  new Clause(new Literal(true, "Alex"), new Literal(false, "Knave"), new Literal(true, "Knight"));
        // (Ben = Knight) ∨ (Ben = Knave) ∨ (Ben = Spy)
        //Clause Cl2 = new Clause(new Literal(true, "BKnave"), new Literal(true, "BKnight"), new Literal(true, "BSpy"));
        // (Cody = Knight) ∨ (Cody = Knave) ∨ (Cody = Spy)
        Clause Cl3 = new Clause(new Literal(true, "CKnave"), new Literal(true, "CKnight"), new Literal(true, "CSpy"));

        // (Alex = Knight) ∧ (Cody = Knave) ⇒ ¬(Ben = Spy) in CNF: (-AKnight V -CKnave V -BSpy)
        Clause Cl4 = new Clause(new Literal(false, "AKnight"), new Literal(false, "CKnave"), new Literal(false, "BSpy"));

        
        
        // (Ben = Knight) ∧ (Alex = Knave) ⇒ ¬(Cody = Spy)
        Clause Cl5 = new Clause(new Literal(false, "BKnight"), new Literal(false, "AKnave"), new Literal(false, "CSpy"));
        // (Cody = Spy) ⇒ ¬(Alex = Knight) ∧ ¬(Ben = Knight)
        Clause Cl6 = new Clause(new Literal(false, "CSpy"), new Literal(false, "AKnight"), new Literal(false, "BKnight"));

        // PROVE Alex
        Clause PROVE = new Clause(new Literal(true, "AKnight"));
        List<Clause> KB = new ArrayList<>();
        KB.addAll(List.of(Cl1, Cl2, Cl3, Cl4, Cl5, Cl6, PROVE));
        return KB;

        // SOLUTION: A is the knight, B is the knave, and C is the spy.
        // SOLUTION2: Cody is the spy.
    }




}
import java.util.ArrayList;
import java.util.List;

class Clause extends ArrayList<Literal>{

    private List<Literal> literals = new ArrayList<>();

    public Clause(List<Literal> literals) {
        this.literals = literals;
    }

    public Clause() {
    }

    public Clause(Literal... literals) {
        for (Literal literal : literals) {
            this.literals.add(literal);
        }
    }

    public Clause(Clause A, Clause B) {
        this.literals.addAll(A.getLiterals());
        this.literals.addAll(B.getLiterals());
    }

    public List<Literal> getLiterals() {
        return literals;
    }

    public void addAll(List<Literal> literals) {
        this.literals.addAll(literals);
    }

    public int getIndex(Literal literal) {
        return literals.indexOf(literal);
    }

    public List<Literal> getPositiveLiterals() {
        List<Literal> positiveLiterals = new ArrayList<>();
        for (Literal literal : literals) {
            if (literal.isPositive()) {
                positiveLiterals.add(literal);
            }
        }
        return positiveLiterals;
    }

    public List<Literal> getNegation(Clause B){
        B.getLiterals();
        // TODO
        return null;
    }

    public List<Literal> getNegativeLiterals() {
        List<Literal> negativeLiterals = new ArrayList<>();
        for (Literal literal : literals) {
            if (!literal.isPositive()) {
                negativeLiterals.add(literal);
            }
        }
        return negativeLiterals;
    }

    public List<Literal> getMatching(Clause B){
        List<Literal> matchingLiterals = new ArrayList<>();
        for (Literal literal : literals) {
            if (B.containsLiteral(literal)) {
                matchingLiterals.add(literal);
            }
        }
        return matchingLiterals;
    }

    public List<Literal> getNegatedMatching(Clause B){
        List<Literal> matchingLiterals = new ArrayList<>();
        for (Literal literal : literals) {
            if (B.containsLiteral(literal.getNegation())) {
                matchingLiterals.add(literal);
            }
        }
        return matchingLiterals;
    }

    public void setLiterals(List<Literal> literals) {
        this.literals = literals;
    }

    public boolean containsLiteral(Literal literal) {
        for (Literal l : literals) {
            if (l.equals(literal)) {
                return true;
            }
        }
        return false;
    }

    public boolean isEmpty() {
        return false;
    }

    public void removeLiteral(Literal literal) {
        if (containsLiteral(literal)){
            literals.remove(literal);
        }
    }

    public void removeDuplicates() {
        List<Literal> newLiterals = new ArrayList<>();
        for (Literal literal : literals) {
            if (!newLiterals.contains(literal)) {
                newLiterals.add(literal);
            }
        }
        literals = newLiterals;
    }

    @Override
    public String toString() {
        return literals.toString();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Clause || ((Clause) obj).getLiterals().size() != literals.size()) {
            Clause clause = (Clause) obj;
            for (Literal literal : literals) {
                if (!clause.containsLiteral(literal)) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }

    public boolean isLowerOrEqual(Clause B) {
        for (Literal literal : literals) {
            if (!B.containsLiteral(literal)) {
                return false;
            }
        }
        return true;
    }
}


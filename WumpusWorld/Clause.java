import java.util.HashSet;
import java.util.Set;

public class Clause {
    private Set<Literal> literals;
    
    public Clause() {
        literals = new HashSet<>();
    }
    
    public void addLiteral(Literal literal) {
        literals.add(literal);
    }
    
    public Set<Literal> getLiterals() {
        return literals;
    }
    
    public boolean isEmpty() {
        return literals.isEmpty();
    }
    
    public static Clause union(Clause c1, Clause c2) {
        Clause result = new Clause();
        result.literals.addAll(c1.literals);
        result.literals.addAll(c2.literals);
        return result;
    }
}   


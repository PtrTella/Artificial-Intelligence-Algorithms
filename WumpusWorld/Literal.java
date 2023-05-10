public class Literal {
    private String symbol;
    private boolean negated;
    
    public Literal(String symbol, boolean negated) {
        this.symbol = symbol;
        this.negated = negated;
    }
    
    public String getSymbol() {
        return symbol;
    }
    
    public boolean isNegated() {
        return negated;
    }
    
    public Literal negate() {
        return new Literal(symbol, !negated);
    }
    
    public boolean equals(Object o) {
        if (o instanceof Literal) {
            Literal other = (Literal) o;
            return symbol.equals(other.symbol) && negated == other.negated;
        }
        return false;
    }
    
    public int hashCode() {
        return symbol.hashCode() + (negated ? 1 : 0);
    }
    
    @Override
    public String toString() {
        return negated ? "~" + symbol : symbol;
    }
    
}

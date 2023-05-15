import java.util.Objects;

class Literal {

    private boolean isPositive;
    private String variable;

    public Literal(boolean isPositive, String variable) {
        this.isPositive = isPositive;
        this.variable = variable;
    }

    public boolean isPositive() {
        return isPositive;
    }

    public void setPositive(boolean isPositive) {
        this.isPositive = isPositive;
    }

    public String getVariable() {
        return variable;
    }

    public void setVariable(String variable) {
        this.variable = variable;
    }

    public Literal getNegation() {
        return new Literal(!isPositive, variable);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Literal literal = (Literal) o;
        return isPositive == literal.isPositive &&
                variable.equals(literal.variable);
    }

    @Override
    public int hashCode() {
        return Objects.hash(isPositive, variable);
    }

    @Override
    public String toString() {
        return isPositive ? variable : "!" + variable;
    }

}

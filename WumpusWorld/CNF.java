import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Stack;

public class CNF {

    // Reduce a sentence to CNF form
    public static List<List<String>> toCNF(String sentence) {
        List<List<String>> cnf = new ArrayList<>();
        // Parse the sentence into a syntax tree
        Node tree = parse(sentence);
        // Convert the tree into CNF form
        Node cnfTree = toCNFHelper(tree);
        // Extract the clauses from the CNF tree
        extractClauses(cnfTree, cnf);
        return cnf;
    }

    private static Node toCNFHelper(Node node) {
        if (node.type == NodeType.LITERAL) {
            // A literal is already in CNF form
            return node;
        } else if (node.type == NodeType.NOT) {
            Node child = toCNFHelper(node.children.get(0));
            if (child.type == NodeType.LITERAL) {
                // A negated literal is also in CNF form
                return node;
            } else if (child.type == NodeType.NOT) {
                // Double negation cancels out
                return child.children.get(0);
            } else if (child.type == NodeType.AND) {
                // De Morgan's Law: ~(A & B) = ~A | ~B
                Node orNode = new Node(NodeType.OR);
                for (Node grandchild : child.children) {
                    Node notGrandchild = new Node(NodeType.NOT);
                    notGrandchild.children.add(grandchild);
                    orNode.children.add(notGrandchild);
                }
                return toCNFHelper(orNode);
            } else if (child.type == NodeType.OR) {
                // De Morgan's Law: ~(A | B) = ~A & ~B
                Node andNode = new Node(NodeType.AND);
                for (Node grandchild : child.children) {
                    Node notGrandchild = new Node(NodeType.NOT);
                    notGrandchild.children.add(grandchild);
                    andNode.children.add(notGrandchild);
                }
                return toCNFHelper(andNode);
            }
        } else if (node.type == NodeType.AND) {
            // Distributive Law: A & (B | C) = (A & B) | (A & C)
            Node orNode = null;
            for (Node child : node.children) {
                Node cnfChild = toCNFHelper(child);
                if (orNode == null) {
                    orNode = new Node(NodeType.OR);
                    for (Node grandchild : cnfChild.children) {
                        Node andNode = new Node(NodeType.AND);
                        andNode.children.add(grandchild);
                        orNode.children.add(andNode);
                    }
                } else {
                    List<Node> andNodes = new ArrayList<>();
                    for (Node grandchild : cnfChild.children) {
                        for (Node orGrandchild : orNode.children) {
                            Node andNode = new Node(NodeType.AND);
                            andNode.children.add(grandchild);
                            andNode.children.add(orGrandchild);
                            andNodes.add(andNode);
                        }
                    }
                    orNode.children = andNodes;
                }
            }
            return orNode;
        } else if (node.type == NodeType.OR) {
            // Distributive Law: A | (B & C) = (A | B) & (A | C)
            Node andNode = null;
            for (Node child : node.children) {
                Node cnfChild = toCNFHelper(child);
                if (andNode == null) {
                    andNode = new Node(NodeType.AND);
                    for (Node grandchild : cnfChild.children) {
                        Node orNode = new Node(NodeType.OR);
                        orNode.children.add(grandchild);
                        andNode.children.add(orNode);
                    }
                } else {
                    List<Node> orNodes = new ArrayList<>();
                    for (Node grandchild : cnfChild.children) {
                        // TODO
                        for (Node andGrandchild : andNode.children) {
                            Node orNode = new Node(NodeType.OR);
                            orNode.children.add(grandchild);
                            orNode.children.add(andGrandchild);
                            orNodes.add(orNode);
                        }
                    }
                    return andNode;
                }
                // Throw an error if the node type is unknown
                throw new IllegalArgumentException("Unknown node type: " + node.type);
            }
        }
        return node;
    }
            
            // Extract the clauses from a CNF tree
            private static void extractClauses(Node node, List<List<String>> clauses) {
                if (node.type == NodeType.AND) {
                    List<String> clause = new ArrayList<>();
                    for (Node child : node.children) {
                        if (child.type == NodeType.LITERAL) {
                            clause.add(child.value);
                        } else if (child.type == NodeType.NOT) {
                            Node literalNode = child.children.get(0);
                            if (literalNode.type == NodeType.LITERAL) {
                                clause.add("!" + literalNode.value);
                            }
                        } else {
                            throw new IllegalArgumentException("Invalid CNF node type: " + child.type);
                        }
                    }
                    clauses.add(clause);
                } else if (node.type == NodeType.OR) {
                    for (Node child : node.children) {
                        extractClauses(child, clauses);
                    }
                } else {
                    throw new IllegalArgumentException("Invalid CNF node type: " + node.type);
                }
            }
            
            // A node in the syntax tree
            private static class Node {
                NodeType type;
                String value;
                List<Node> children;
            
                Node(NodeType type) {
                    this.type = type;
                    this.value = null;
                    this.children = new ArrayList<>();
                }
            
                Node(NodeType type, String value) {
                    this.type = type;
                    this.value = value;
                    this.children = new ArrayList<>();
                }
            }
            
            // Enum for the types of nodes in the syntax tree
            private enum NodeType {
                LITERAL,
                NOT,
                AND,
                OR,
                OPEN,
                CLOSE
            }

            // Parse a sentence into a syntax tree
            private static Node parse(String sentence) {
                String[] tokens = sentence.split("\\s+");
                Stack<Node> stack = new Stack<>();
                for (String token : tokens) {
                    if (token.equals("(")) {
                        stack.push(new Node(NodeType.OPEN));
                    } else if (token.equals(")")) {
                        Node node = stack.pop();
                        if (node.type == NodeType.NOT) {
                            Node child = stack.pop();
                            node.children.add(child);
                        } else if (node.type == NodeType.AND || node.type == NodeType.OR) {
                            List<Node> children = new ArrayList<>();
                            while (stack.peek().type != node.type) {
                                children.add(stack.pop());
                            }
                            children.add(node);
                            Collections.reverse(children);
                            node.children = children;
                        }
                        stack.pop(); // remove the OPEN node
                        stack.push(node);
                    } else if (token.equals("!")) {
                        stack.push(new Node(NodeType.NOT));
                    } else if (token.equals("&")) {
                        stack.push(new Node(NodeType.AND));
                    } else if (token.equals("|")) {
                        stack.push(new Node(NodeType.OR));
                    } else {
                        stack.push(new Node(NodeType.LITERAL, token));
                    }
                }
                return stack.pop();
            }
            
}
            
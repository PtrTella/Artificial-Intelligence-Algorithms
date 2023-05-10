import java.util.ArrayList;
import java.util.List;

public class NodeS {
    private NodeType type;
    private List<Node> children;

    public Node(NodeType type, List<Node> children) {
        this.type = type;
        this.children = children;
    }

    public Node(NodeType type) {
        this(type, new ArrayList<Node>());
    }

    public NodeType getType() {
        return type;
    }

    public List<Node> getChildren() {
        return children;
    }

    public void addChild(Node child) {
        children.add(child);
    }
}



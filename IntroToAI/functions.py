import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# Minimal Problem and Node definitions
class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        # Must be overridden by subclasses
        raise NotImplementedError

    def result(self, state, action):
        # Must be overridden by subclasses
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def action_cost(self, s, action, s1):
        return 1  # default cost

    def h(self, state):
        # Default heuristic is zero
        return 0


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def expand(problem, node):
    """Generate the children nodes for a given node."""
    for action in problem.actions(node.state):
        new_state = problem.result(node.state, action)
        cost = node.path_cost + problem.action_cost(node.state, action, new_state)
        yield Node(new_state, node, action, cost)

def path_actions(node):
    """Return the list of actions from the root to the node."""
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]

def path_states(node):
    """Return the list of states from the root to the node."""
    if node.parent is None:
        return [node.state]
    return path_states(node.parent) + [node.state]


# A simple UndirectedGraph class that ensures symmetry.
class UndirectedGraph(dict):
    def __init__(self, graph_dict=None):
        super().__init__(graph_dict or {})
        if graph_dict:
            # For each edge (u->v), ensure there is an edge (v->u)
            for u in list(graph_dict.keys()):
                for v, cost in graph_dict[u].items():
                    if v not in self:
                        self[v] = {}
                    if u not in self[v]:
                        self[v][u] = cost


def plot_map(map_obj, solution=None, expanded=None, title="Map", show=True):
    """
    Visualize the map using the provided undirected graph and locations.
    
    Args:
        map_obj (UndirectedGraph): The graph of nodes with their connections and a 'locations' attribute.
        solution (list, optional): A list of node names representing the solution path.
        expanded (list, optional): A list of node names that were expanded during search.
        title (str): Title for the plot.
        show (bool): Whether to call plt.show() at the end.
    """
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 8))
    
    # Plot all edges and label with cost.
    for city, neighbors in map_obj.items():
        if city not in map_obj.locations:
            continue
        for neighbor, cost in neighbors.items():
            if neighbor not in map_obj.locations:
                continue
            if city < neighbor:  # draw each edge only once
                x1, y1 = map_obj.locations[city]
                x2, y2 = map_obj.locations[neighbor]
                plt.plot([x1, x2], [y1, y2], color="gray", lw=1, alpha=0.5)
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                plt.text(mid_x, mid_y, str(cost), fontsize=8, color="purple")
    
    # Plot nodes and label them.
    for city, (x, y) in map_obj.locations.items():
        plt.plot(x, y, 'ko', markersize=4)
        plt.text(x+2, y+2, city, fontsize=8, color='black')
    
    # Mark expanded nodes if provided.
    if expanded:
        expanded_coords = [map_obj.locations[city] for city in expanded if city in map_obj.locations]
        if expanded_coords:
            xs, ys = zip(*expanded_coords)
            # Using cyan circles for expanded nodes.
            plt.scatter(xs, ys, s=100, color='cyan', marker='o', label="Expanded")
    
    # If a solution path is provided, highlight it.
    if solution:
        sol_coords = [map_obj.locations[city] for city in solution if city in map_obj.locations]
        if sol_coords:
            xs, ys = zip(*sol_coords)
            plt.plot(xs, ys, 'r-', lw=2, label="Solution Path")
            # Mark the start and goal with star markers.
            start = solution[0]
            goal = solution[-1]
            start_x, start_y = map_obj.locations[start]
            goal_x, goal_y = map_obj.locations[goal]
            plt.plot(start_x, start_y, 'g*', markersize=15, label="Start")
            plt.plot(goal_x, goal_y, 'r*', markersize=15, label="Goal")
            plt.legend()
    
    plt.title(title)
    if show:
        plt.show()




# --------------------
# Tkinter-based Animation (Expansion Stepwise, then one Red Line for Solution)
# --------------------

def animate_route_problem_with_expansion(problem, map_obj, algorithm, pause_time=1000):
    # Run modified A* search to get solution and expansion list.
    solution_node, expansion_list = algorithm(problem)
    if not solution_node:
        print("No solution found.")
        return
    sol_path = path_states(solution_node)
    print("Solution Path:", " -> ".join(sol_path))
    print("Total cost:", solution_node.path_cost)
    
    # Create the Tkinter window.
    root = tk.Tk()
    root.title("Route Problem Animation")
    
    # Create a matplotlib figure and embed it.
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw the map: edges (with cost labels) and nodes.
    for city, neighbors in map_obj.items():
        if city not in map_obj.locations:
            continue
        for neighbor, cost in neighbors.items():
            if neighbor not in map_obj.locations:
                continue
            if city < neighbor:
                x1, y1 = map_obj.locations[city]
                x2, y2 = map_obj.locations[neighbor]
                ax.plot([x1, x2], [y1, y2], color="gray", lw=1, alpha=0.5)
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                ax.text(mid_x, mid_y, str(cost), fontsize=8, color="purple")
                
    for city, (x, y) in map_obj.locations.items():
        ax.plot(x, y, 'ko', markersize=4)
        ax.text(x+2, y+2, city, fontsize=8, color="black")
    
    # Mark start and goal.
    ax.plot(*map_obj.locations[problem.initial], 'g*', markersize=15, label="Start")
    ax.plot(*map_obj.locations[problem.goal], 'r*', markersize=15, label="Goal")
    ax.legend()
    ax.set_title(f"Route Problem Animation - {algorithm.__name__} with Expansion")
    
    # Embed the figure in Tkinter.
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()
    
    # Animate node expansion stepwise.
    total_expansion = len(expansion_list)
    current_index = [0]
    
    def animate_expansion():
        if current_index[0] < total_expansion:
            # Get expanded nodes up to current index.
            pts = [map_obj.locations[s] for s in expansion_list[:current_index[0]+1] if s in map_obj.locations]
            # Remove any previous expansion scatter objects.
            for coll in list(ax.collections):
                if coll.get_label() == "Expanded":
                    coll.remove()
            if pts:
                ax.scatter(*zip(*pts), s=100, color='blue', label="Expanded")
            canvas.draw()
            current_index[0] += 1
            root.after(pause_time, animate_expansion)
        else:
            # Once expansion is complete, draw the final solution path as one red line.
            sol_coords = [map_obj.locations[s] for s in sol_path if s in map_obj.locations]
            if sol_coords:
                xs, ys = zip(*sol_coords)
                ax.plot(xs, ys, 'r-', lw=2, label="Solution Path")
                canvas.draw()
            print("Animation complete.")
    
    animate_expansion()
    root.mainloop()
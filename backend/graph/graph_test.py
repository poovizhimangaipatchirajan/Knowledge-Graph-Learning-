from graph_visualizer import create_graph_html

sample = [
    {
        "scheme": "ISOPOM",
        "beneficiary": "Farmers",
        "benefit_type": "Seed Subsidy",
        "funding": "₹1000 per quintal"
    }
]

create_graph_html(sample)

print("Graph Created")
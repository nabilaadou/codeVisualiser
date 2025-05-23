// @ts-ignore
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';

export function	generateDiagram(tree : JSON) {
	const width = 800;
	const height = 400;
	const topMargin = 40;
	
	const svg = d3.create('svg')
		.attr('height', height)
		.attr('width', width);
	
	const root = d3.hierarchy(tree);
	const treeLayout = d3.tree().size([width, height - topMargin]);
	treeLayout(root);
	
	const g = svg.append("g")
		.attr("transform", `translate(0, ${topMargin})`);

	g.selectAll('.links')
		.data(root.links())
		.join('path')
			.attr('class', 'links')
			.attr("fill", "none")
      		.attr("stroke", 'green')
      		.attr("stroke-opacity", 0.6)
      		.attr("stroke-width", 0.8)
			.attr('d', d3.linkVertical()
				.x(d => d.x)
				.y(d => d.children ? d.y : d.y - 17)
			);
	
	const nodes = g.selectAll("g.nodes")
		.data(root.descendants())
			.join('g')
			.attr('class', 'nodes')
			.attr('transform', d => `translate(${d.x}, ${d.y})`);
	
	nodes.append('text')
		.attr('text-anchor', 'middle')
		.text(d => d.data.name);

	// Append SVG to body
	d3.select('body')
	  .append(() => svg.node());
	
}
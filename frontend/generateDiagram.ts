// @ts-ignore
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';

export function	generateDiagram(tree : JSON) {
	const root = d3.hierarchy(tree);
	console.log(root);
	// const svg = d3.select("body")
	// .append("svg");

	// svg.append("circle")
	// .attr("cx", 50)
	// .attr("cy", 50)
	// .attr("r", 40)
	// .attr("fill", "red");
	
}
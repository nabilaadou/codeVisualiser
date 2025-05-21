// @ts-ignore
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';

export function	generateDiagram(tree : JSON) {
	const body = d3.select("body");
	body.append("p")
	.text("hello new paragraph added");
}
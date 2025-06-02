// @ts-ignore
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';

export function	generateDiagram(tree : JSON) {
	// figure out how to now be ontop of the help box
	// removing the upload page
	d3.select('#uploadPage').remove();	
	d3.select('#userGuide').remove();

	const svg = d3.create('svg')
		.attr('height', '100vh')
		.attr('width', '100vw');

	const root = d3.hierarchy(tree);
	const treeLayout = d3.tree().nodeSize([200, 150]); //width , height
	treeLayout(root);
	
	const centerX = window.innerWidth / 2;
	const centerY = window.innerHeight / 2;

	const g = svg.append("g")
					.attr('id', 'diagram');

	g.selectAll('.links')
		.data(root.links())
		.join('path')
			.attr('class', 'links')
			.attr("fill", "none")
      		.attr("stroke", 'green')
      		.attr("stroke-opacity", 0.6)
      		.attr("stroke-width", 0.8)
			.attr('d', d3.linkVertical()
				.x(d => d.x + centerX)
				.y(d => d.y + centerY)
			);
	
	const nodes = g.selectAll("g.nodes")
		.data(root.descendants())
			.join('g')
			.attr('class', 'nodes')
			.attr('transform', d => `translate(${d.x + centerX}, ${d.y + centerY})`);
	
	nodes.on('click', function(_, d) {
		infosBar(d, centerX, centerY);
	});

	nodes.append('text')
		.attr('text-anchor', 'middle')
		.text(d => d.data.name);

	const zoom = d3.zoom()
		.on('zoom', (event) => {
			g.attr('transform', event.transform);
		});
	
	svg.call(zoom)
	
	//removing any existant svg
	d3.select('svg').remove()
	// Append SVG to body
	d3.select('body')
	  .append(() => svg.node());
	
}

function	infosBar(d, centerX, centerY) {
	//remove any shown bar
	const bar = document.getElementById('nodeBar');
	if (bar)
		bar.remove();
	else {
		const diagram = document.getElementById('diagram');

		const g = document.createElementNS('http://www.w3.org/2000/svg','g');
		g.id = 'nodeBar';
		g.setAttribute('transform', `translate(${d.x + centerX}, ${d.y + centerY - 120})`);

		const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
		rect.setAttribute('fill', 'lightblue');
		rect.setAttribute('opacity', '0.3');
		rect.setAttribute('width', '90px');
		rect.setAttribute('height', '100px');

		const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		text.textContent = 'info';
		text.setAttribute('text-anchor', 'middle');

		g.appendChild(rect);
		g.appendChild(text);
		diagram.appendChild(g);
	}
}
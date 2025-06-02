import { generateDiagram } from './generateDiagram.js'

type filesInfo = {
	fileName: string;
	content: string;
};

async function sendDataToBackend(folder : FileList, file : string) {
	let		res;
	const data = {
		folder: {},
		file: file
	};

	for (let i = 0; i < folder.length; i++) {
		const file = folder[i];
		const fileContent = await file.text();
		data.folder[file.name] = fileContent;
	}
	try {
		res = await fetch('http://localhost:8000/pySourceFiles', {
			method: 'POST',
			headers: {
				'Content-type': 'application/json'
			},
			body: JSON.stringify(data)
  		});
	} catch (err) {
		console.log('Error: ', err);
	}
	return res;
}

export function formElements(formElement : HTMLFormElement, folderInputElement : HTMLInputElement, fileInputElement : HTMLInputElement) {
	formElement.addEventListener('submit', async (event) => {
		event.preventDefault(); // to prevent the page from refreshing

		const	folder = folderInputElement.files;
		const	file = fileInputElement.value;
		if (!folder || folder.length === 0) {
			console.log('No folder selected.');
			return;
		} else if (file == '') {
			console.log('no file were selected')
			return;
		}
		
		const	res = await sendDataToBackend(folder, file);
		const	codeTree = await res.json();
		
		console.log('Submit complete, server responded with:', codeTree);
		generateDiagram(codeTree)
		return codeTree;
	});
}
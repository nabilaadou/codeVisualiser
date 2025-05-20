const form = document.getElementById('uploadForm') as HTMLFormElement;
const fileInput = document.getElementById('fileInput') as HTMLInputElement;

type filesInfo = {
	fileName: string;
	content: string;
};

async function sendFilePaths(filesPaths : filesInfo[]) {
	let	res;
	try {
		res = await fetch('http://localhost:8000/diagram', {
			method: 'POST',
			headers: {
				'Content-type': 'application/json'
			},
			body: JSON.stringify(filesPaths)
  		});
	} catch (err) {
		console.log('Error: ', err);
	}
	return res;
}

async function handleSubmitEvent(files : FileList) {
	const	info : filesInfo[] = [];

	for (let i = 0; i < files.length; i++) {
		const file = files[i];
		const fileContent = await file.text();
		info.push({fileName: file.name, content: fileContent}) // cast needed for TS
	}
	const res = await sendFilePaths(info);
	return res;
}

form.addEventListener('submit', async (event) => {
	event.preventDefault(); // to prevent the page from refreshing

	const	files = fileInput.files;
	if (!files || files.length === 0) {
		console.log('No files selected.');
		return;
	}

	const	res = await handleSubmitEvent(files);
	const	resolvedRes = await res.json();
	
	console.log('Submit complete, server responded with:', resolvedRes);
	return resolvedRes;
});
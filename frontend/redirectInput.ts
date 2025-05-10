const form = document.getElementById('uploadForm') as HTMLFormElement;
const fileInput = document.getElementById('fileInput') as HTMLInputElement;

type fileRelativePath = {
	path: string;
	content: string;
};

async function sendFilePaths(filesPaths : fileRelativePath[]) {
	let res;
	try {
		res = await fetch('http://localhost:8000/diagram', {
			method: 'POST',
			headers: {
				'Content-type': 'application/json'
			},
			body: JSON.stringify(filesPaths)
  		});
		const data = await res.json();
		console.log('Server response:', data);
	} catch (err) {
		console.log('Error: ', err);
	}
	return res;
}

async function handleSubmitEvent() {
	const files = fileInput.files;
	if (!files || files.length === 0) {
		console.log('No files selected.');
		return;
	}

	const filesPaths : fileRelativePath[] = [];

	for (let i = 0; i < files.length; i++) {
		const file = files[i];
		const fileContent = await file.text();
		filesPaths.push({path: (file as any).webkitRelativePath, content: fileContent}) // cast needed for TS
	}
	const res = await sendFilePaths(filesPaths);
	return res;
}

form.addEventListener('submit', async (event) => {
	const res = await handleSubmitEvent();
	console.log('Submit complete, server responded with:', res);
	return res;
});
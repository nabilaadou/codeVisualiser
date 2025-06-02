// @ts-ignore
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm';
import { formElements } from "./redirectInput.js"

const	uploadMenu = document.getElementById('uploadMenu') as HTMLButtonElement

uploadMenu.addEventListener('click', (event: Event) => {
    event.preventDefault();

    const	outerDiv = document.createElement('div');
	outerDiv.setAttribute('id', 'uploadPage')
    outerDiv.style.position = 'fixed';
    outerDiv.style.top = '0';
    outerDiv.style.left = '0';
    outerDiv.style.width = '100vw';
    outerDiv.style.height = '100vh';
    outerDiv.style.display = 'flex';
    outerDiv.style.justifyContent = 'center';
    outerDiv.style.alignItems = 'center';
    outerDiv.style.background = 'rgba(0, 0, 0, 0.5)';
    outerDiv.style.zIndex = '999';

    const	innerDiv = document.createElement('div');
    innerDiv.style.backgroundColor = '#f9f9f9';
    innerDiv.style.width = '40vw';
    innerDiv.style.height = '60vh';
    innerDiv.style.borderRadius = '12px';
    innerDiv.style.fontFamily = 'sans-serif';
    innerDiv.style.display = 'flex';
    innerDiv.style.flexDirection = 'column';
    innerDiv.style.alignItems = 'center';

    const	img = document.createElement('img');
    img.style.width = '2cm';
    img.style.height = '2cm';
    img.style.marginTop = '3cm';
    img.src = './assets/upload_icon.png';

    const	h3 = document.createElement('h3');
    h3.style.margin = '0';
    h3.style.marginTop = '1cm';
    h3.textContent = 'Select Project Folder';

    const	form = document.createElement('form');
    form.style.display = 'flex';
    form.style.flexDirection = 'column';
    form.style.alignItems = 'center';

    const	folderInput = document.createElement('input');
    folderInput.style.marginTop = '0.4cm';
    folderInput.type = 'file';
    folderInput.setAttribute('webkitdirectory', 'true');

	const	fileInputLabel = document.createElement('p');
	fileInputLabel.textContent = 'select file to compile';
	fileInputLabel.style.fontSize = '14px';
	fileInputLabel.style.margin = '0';
	fileInputLabel.style.marginTop = '0.3cm';

	const	fileInput = document.createElement('input');
    fileInput.style.marginTop = '0.1cm';
    fileInput.type = 'text';
	fileInput.setAttribute('placeholder', 'eg: main.py');
	fileInput.setAttribute('List', 'fileSuggestions');

    const dataList = document.createElement('datalist');
    dataList.setAttribute('id', 'fileSuggestions');

    const	submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.style.marginTop = '2.7cm';
    submitButton.style.border = 'none';
    submitButton.style.borderRadius = '5px';
    submitButton.style.width = '3cm';
    submitButton.style.height = '0.8cm';
    submitButton.style.color = 'white';
    submitButton.style.backgroundColor = 'coral';
    submitButton.textContent = 'Upload';

	//appending elements to their parents
    form.appendChild(folderInput);
    form.appendChild(fileInputLabel);
    form.appendChild(fileInput);
    form.appendChild(dataList);
    form.appendChild(submitButton);
    
    // innerDiv.appendChild(exitButton);
    innerDiv.appendChild(img);
    innerDiv.appendChild(h3);
    innerDiv.appendChild(form);
    
    outerDiv.appendChild(innerDiv);
    
    document.body.appendChild(outerDiv);
	formElements(form, folderInput, fileInput);


    outerDiv.addEventListener('click', (event) => {
        const element = event.target as HTMLElement;
        if (element.id == 'uploadPage')
            outerDiv.remove();
    })

    folderInput.addEventListener('change', () => {
        if (folderInput.files.length > 0) {
            dataList.innerHTML = '' //removing any previous assigned options
            for (let i = 0; i < folderInput.files.length; ++i) {
                const option = document.createElement('option');
                option.setAttribute('value', folderInput.files[i].name);
                dataList.appendChild(option);
            }
        } else {
            console.log('no folder was selected');
        }
    })
});

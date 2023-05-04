const tracker_type = document.getElementById('tracker_type')
const settings = document.getElementById('settings');
const hiddenInput = document.getElementById("tracker_settings");


window.onload = function(){
    console.log("INSIDE ONLOAD ** ")
    tracker_settings();
};
tracker_type.addEventListener('change', function(){
    console.log("INSIDE CHANGE ** ")
    removeAllChildNodes(settings);
    tracker_settings();
});


function removeAllChildNodes(parent) {
    hiddenInput.value = '';
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function tracker_settings(){
   
    let tracker_val = tracker_type.value
    
    if(tracker_val == 'Boolean'){
        return;
    }

    settings.innerHTML += '<p style="text-decoration:underline"> Settings </p>'
    let labelNode = document.createElement("label");
    let inputNode = document.createElement("input");
    let selectNode = document.createElement('select');
    let textNode = document.createTextNode('');
    labelNode.appendChild(textNode);
    inputNode.id = 'settings_val';
    inputNode.type = 'text';
    settings.appendChild(labelNode);

    //in case of the edit tracker form 
    if(hiddenInput.value.length != 0){
        console.log("Inside hidden input *** ");
        inputNode.value = hiddenInput.value;
    }

    if(tracker_val == 'Numerical'){
        textNode.nodeValue = 'Set a unit:';
        if(hiddenInput.value.length != 0){
            console.log("Inside hidden input *** ");
            inputNode.value = hiddenInput.value;
        }
        settings.append(labelNode, inputNode);
    }
    else if(tracker_val == 'Multiple Choice'){
        textNode.nodeValue = 'Add options:'
        inputNode.placeholder = 'Eg. option1,option2,...'
        settings.append(labelNode, inputNode);
    }
    else if(tracker_val == 'Time Duration'){
        textNode.nodeValue = 'Set time unit:'
        selectNode.id = 'settings_val';
        let option1 = document.createElement('option');
        let option2 = document.createElement('option');
        let option3 = document.createElement('option');
        option1.appendChild(document.createTextNode('hours'));
        option2.appendChild(document.createTextNode('minutes'));
        option3.appendChild(document.createTextNode('seconds'));
        selectNode.append(option1,option2, option3);
        settings.appendChild(selectNode);
      
    }
    let elem = document.getElementById("settings_val");
    let tracker_form = document.getElementById("tracker-form")
    tracker_form.onsubmit = function(){
        hiddenInput.value = elem.value;
    }

}
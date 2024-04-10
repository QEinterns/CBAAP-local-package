document.addEventListener('DOMContentLoaded', function() {
    const steps = document.querySelectorAll('.step');
    const prevBtns = document.querySelectorAll('.prevBtn');
    const nextBtns = document.querySelectorAll('.nextBtn');
    const startBtn = document.querySelector('.cool-button'); // Get the "Start" button
    const loader = document.getElementById('loader');
    const progressBar = document.getElementById('progress');
    let currentStep = 0;
    let modelName=""
    let context = ""
    let iterationCount = 0
    let ollamaName =""
    let quantizeLevel = ""
    const pdfInput = document.getElementById('pdfInput');
    const fileList = document.getElementById('fileList');

    function navigateToStep6() {
        const steps = document.querySelectorAll('.step');
        const progressBar = document.getElementById('progress');
    
        // Hide all steps except step 6
        steps.forEach(function(step, index) {
            if (index == 5) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    
        // Update progress bar to indicate step 6 completion
        const progress = (6) / (steps.length) * 100; // Assuming there are 6 steps in total
        progressBar.style.width = progress + '%';
    }

    
    function startLoader() {
        document.getElementById("loader").style.display = "block";
    }
    
    function stopLoader() {
        document.getElementById("loader").style.display = "none";
    }


    pdfInput.addEventListener('change', function() {
        Array.from(pdfInput.files).forEach(function(file) {
            const fileCard = createFileCard(file);
            fileList.appendChild(fileCard);
        });
    });

    function createFileCard(file) {
        const fileCard = document.createElement('div');
        fileCard.classList.add('file-card');
        const fileName = document.createElement('span');
        fileName.textContent = file.name;
        fileCard.appendChild(fileName);
        return fileCard;
    }

    // Function to show the current step
    function showStep(stepIndex) {
        steps.forEach(function(step, index) {
            if (index === stepIndex) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Update progress bar    
        const progress = (stepIndex) / (steps.length) * 100;
        progressBar.style.width = progress + '%';
    }

    // Initial step display
    showStep(currentStep);

    // Function to handle previous button click
    prevBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            currentStep--;
            if (currentStep < 0) {
                currentStep = 0;
            }
            showStep(currentStep);
        });
    });

    // Function to handle next button click
    nextBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            // Perform necessary actions based on current step
            if (currentStep === 0) {
                // Handle step 1 actions
                // For demo, just directly move to next step
                currentStep++;
            } else if (currentStep === 1) {
                // Handle step 2 actions
                // Validate model selection before moving to next step
                const selectedModel = document.querySelector('input[name="model"]:checked');
                if (selectedModel) {
                    console.log(selectedModel.value)
                    modelName  = selectedModel.value
                    // For demo, just directly move to next step
                    currentStep++;
                } else {
                    alert('Please select a model');
                    return; // Stop execution if model is not selected
                }
            } else if (currentStep === 2) {
                // Handle step 3 actions
                // Validate file uploads and context field before moving to next step
                const pdfInput = document.getElementById('pdfInput');
                const context_a = document.getElementById('context').value.trim();
                console.log(context)
                context  =context_a
                // Log file names for PDF inputs
                const files = Array.from(pdfInput.files);

                // Create an array to store all fetch promises
                const uploadPromises = [];

                files.forEach(function(file) {
                    console.log("File Name:", file.name);
                    // Store PDFs in a specific folder (Assuming you have a server-side script to handle file upload)
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    // Create a fetch promise for each file and push it to the uploadPromises array
                    const uploadPromise = fetch('/upload_finetune', {
                        method: 'POST',
                        body: formData
                    }).then(response => {
                        if (response.ok) {
                            console.log('PDF Uploaded successfully');
                        } else {
                            console.error('Failed to upload PDF');
                        }
                    }).catch(error => {
                        console.error('Error:', error);
                    });

                    uploadPromises.push(uploadPromise);
                });

                // Wait for all fetch requests to complete
                Promise.all(uploadPromises)
                    .then(() => {
                        console.log('All PDFs uploaded successfully');
                    })
                    .catch(error => {
                        console.error('Error uploading PDFs:', error);
                    });
                currentStep++;
            } else if (currentStep === 3) {
                // Handle step 4 actions
                // Logging all input values
                // console.log("Input Values:");
                // const inputs = document.querySelectorAll('#step4 input[type="text"], #step4 input[type="radio"]:checked');
                // // cc = 0
                // inputs.forEach(function(input) {
                //     // if(cc==0){
                //     //     iterationCount = input.value
                //     // }
                //     // else if(cc==1){
                //     //     ollamaName = input.value
                //     // }
                //     // else{
                //     //     quantizeLevel = input.value
                //     // }
                //     // cc++;
                //     console.log(input.value);
                // });

                
                // Log other specific input values or perform additional actions if needed

               currentStep++;
            }else{
                currentStep++;
            }

            // Update step display
            showStep(currentStep);
        });
    });

    // Event listener for the "Start" button
    // startBtn.addEventListener('click', function() {
    //     // Logging all input values
    //     // console.log("Input Values:");
    //     // const inputs = document.querySelectorAll('#step4 input[type="text"], #step4 input[type="radio"]:checked');
    //     // inputs.forEach(function(input) {
    //     //     console.log(input.name + ":", input.value);
    //     // });
    //     console.log("Input Values:");
    //             const iterationsInput = document.getElementById('iterations');
    //             const preferredModelInput = document.getElementById('preferredModel');
    //             const quantizeInputs = document.querySelectorAll('#quantize_form input[type="radio"]:checked');
    //             const quan_value = document.querySelector('input[name="quan"]:checked').value;
    //             console.log(quantizeInputs)
    //             const iterationsValue = iterationsInput.value;
    //             const preferredModelValue = preferredModelInput.value;
                
             
                

    //     fetch('/start', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //             modelName: modelName,
    //             context: context,
    //             iterationCount: iterationsValue,
    //             ollamaName: preferredModelValue,
    //             quantizeLevel: quan_value
    //         })
    //     })
    //     .then(response => {
    //         if (response.ok) {
    //             console.log('Data sent to server successfully');
    //         } else {
    //             console.error('Failed to send data to server');
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //     });
        
    // });

    startBtn.addEventListener('click', function() {
        // Show the loader when the button is clicked
        const progress = (4) / (steps.length) * 100;
        progressBar.style.width = progress + '%';

        steps.forEach(function(step, index) {
            if (index ===4) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
        // Logging all input values
        console.log("Input Values:");
        const iterationsInput = document.getElementById('iterations');
        const preferredModelInput = document.getElementById('preferredModel');
        const quantizeInputs = document.querySelectorAll('#quantize_form input[type="radio"]:checked');
        const quan_value = document.querySelector('input[name="quan"]:checked').value;
        console.log(quantizeInputs)
        const iterationsValue = iterationsInput.value;
        const preferredModelValue = preferredModelInput.value;
    
        // Send data to the server using fetch
        fetch('/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                modelName: modelName,
                context: context,
                iterationCount: iterationsValue,
                ollamaName: preferredModelValue,
                quantizeLevel: quan_value
            })
        })
        .then(response => {
            if (response.ok) {
                console.log('Data sent to server successfully');
                // var param1 = iterationsValue.toString();
                // var param2 = preferredModelValue;
                // // console.log
                stopLoader();
                // // Construct the URL with parameters
                // // var url = "{{ url_for('download_direct', " + "param1="+param1 + ", param2=" + param2+") }}";
                // var url = "{{url_for('download_direct', param1=1, param2=p1)}}";
                // console.log(url)
                // // Update the href attribute of the button
                // document.getElementById('downloadButton').setAttribute('href', url);

                var param1 = encodeURIComponent(iterationsValue.toString());
                var param2 = encodeURIComponent(preferredModelValue);

                var url = "/download_i?param1=" + param1 + "&param2=" + param2;

                // Redirect the browser to the constructed URL
                window.location.href = url;

                var step5Div = document.getElementById('step5');
                step5Div.innerHTML = ""; // Clear existing content

                // Create h2 element for the text "Model downloaded!"
                var h2Element = document.createElement('h2');
                h2Element.textContent = "Model downloaded!";
                step5Div.appendChild(h2Element); // Append h2 element to step5 div

                // Create success tick animation
                var successTick = document.createElement('div');
                successTick.classList.add('success-tick'); // Add class for styling
                step5Div.appendChild(successTick); 

                const progress = 100; // Assuming there are 6 steps in total
                progressBar.style.width = progress + '%';

                // Hide the loader when the response is received
                // stopLoader();
                // navigateToStep6();
            } else {
                console.error('Failed to send data to server');
                // Hide the loader in case of an error
                // stopLoader();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Hide the loader in case of an error
            // stopLoader();
        });

        
    });
});

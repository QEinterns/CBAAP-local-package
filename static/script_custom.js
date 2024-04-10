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

    let host_address = ""
    let host_type = ""
    let username  = ""
    let password = ""
    let bucket = ""
    let scope = ""
    let collection = ""
    let index_name = ""
    let embedding_model = ""
    let ip_addr = ""
    let app_name = ""





    
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
            if (currentStep === 0) {
                currentStep++;


            } else if (currentStep === 1) {

                const host = document.querySelector('input[name="couchbase-host"]:checked');
                if (host) {
                    console.log(host.value)
                    host_type = host.value
                    currentStep++;
                } else {
                    alert('Please select the host type');
                    return;
                }

            } else if (currentStep === 2) {

                app_name = document.getElementById('app_name').value;
                username = document.getElementById('username').value;
                password = document.getElementById('password').value;
                ip_addr = document.getElementById('ip_addr').value;
                bucket = document.getElementById('bucket').value;

                console.log(username)
                console.log(password)
                console.log(ip_addr)
                console.log(bucket)

                currentStep++;
            } else if (currentStep === 3) {


                scope = document.getElementById('scope').value;
                collection = document.getElementById('collection').value;
                index_name = document.getElementById('index_name').value;
                embedding_model = "baai"

                currentStep++;
            }else if(currentStep ===  4){
                const pdfInput = document.getElementById('pdfInput');
                const context_a = document.getElementById('context').value.trim();
                console.log(context)
                context  =context_a



                Array.from(pdfInput.files).forEach(function(file) {
                    console.log("File Name:", file.name);
                    const formData = new FormData();
                    formData.append('file', file);
                    fetch('/upload_fine', {
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
                });
                currentStep++;

                
            }else if (currentStep === 5) {

        
                currentStep++;
            } else if (currentStep === 6) {
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

            showStep(currentStep);
        });
    });


    startBtn.addEventListener('click', function() {
        // Show the loader when the button is clicked

        document.getElementById("uploadForm").submit();


        const progress = (7) / (steps.length) * 100;
        progressBar.style.width = progress + '%';

        steps.forEach(function(step, index) {
            if (index ===7) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
        // Logging all input values
        const pdfInput = document.getElementById('pdfInput');
        const context_a = document.getElementById('context').value.trim();
        console.log(context)
        context  =context_a

        const uploadPromises = [];

        // Array.from(pdfInput.files).forEach(function(file) {
        //     console.log("File Name:", file.name);
        //     const formData = new FormData();
        //     formData.append('file', file);

        //     uploadPromises.push(
        //     fetch('/upload_fine', { 
        //         method: 'POST',
        //         body: formData
        //     }).then(response => {
        //         if (response.ok) {
        //             console.log('PDF Uploaded successfully');
        //         } else {
        //             console.error('Failed to upload PDF');
        //         }
        //     }).catch(error => {
        //         console.error('Error:', error);
        //     })
        // );
        // });

        // Promise.all(uploadPromises)
        // .then(() => {
            console.log('All PDFs uploaded successfully');
            currentStep++; // Move to the next step
    
            // Send data to the server only after all PDFs are uploaded
            fetch('/create_app_inputs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    modelName: "ehidwbf",
                    context: context,
                    iterationCount: 0,
                    ollamaName: "jofhg",
                    quantizeLevel: "ihjdwsf",
                    username: username,
                    password: password,
                    ip_addr: ip_addr,
                    bucket: bucket,
                    scope: scope,
                    collection: collection,
                    index_name: index_name,
                    embedding_model: embedding_model,
                    host_type: host_type,
                    app_name: app_name
                })
            })
            .then(response => response.json())
            .then(data => {
                // Redirect to the result page
                window.location.href = data.redirect_url;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        // })
        // .catch(error => {
        //     console.error('Error during file upload:', error);
        // });
        
        
        // .then(response => {
        //     if (response.ok) {
        //         console.log('Data sent to server successfully');
        //         stopLoader();

               
        //         // return "great"
        //         // var param1 = encodeURIComponent(iterationsValue.toString());
        //         // var param2 = encodeURIComponent(preferredModelValue);
        //         // var url = "/download_i?param1=" + param1 + "&param2=" + param2;

        //         // // Redirect the browser to the constructed URL
        //         // window.location.href = url;

        //         // var step5Div = document.getElementById('step5');
        //         // step5Div.innerHTML = ""; // Clear existing content

        //         // // Create h2 element for the text "Model downloaded!"
        //         // var h2Element = document.createElement('h2');
        //         // h2Element.textContent = "Model downloaded!";
        //         // step5Div.appendChild(h2Element); // Append h2 element to step5 div

        //         // // Create success tick animation
        //         // var successTick = document.createElement('div');
        //         // successTick.classList.add('success-tick'); // Add class for styling
        //         // step5Div.appendChild(successTick); 
        //         // // Hide the loader when the response is received
        //         // // stopLoader();
        //         // // navigateToStep6();
        //     } else {
        //         console.error('Failed to send data to server');
        //         // Hide the loader in case of an error
        //         // stopLoader();
        //     }
        // })
        // .catch(error => {
        //     console.error('Error:', error);
        //     // Hide the loader in case of an error
        //     // stopLoader();
        // });

        
    });
});

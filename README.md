
![Logo](https://upload.wikimedia.org/wikipedia/commons/b/bc/Couchbase_logo.png)


# CBAAP

CBAAP stands for 'CouchBase AI App Playground' where you have AI apps which leverages the Couchbase Vector Search feature which is released in Couchbase 7.6.0. Before starting off with this, we highly recommend you to check the below documentations on how each app is built so that you get a clear idea about the apps before using them.



## Documentation

 - [Imagine](https://docs.google.com/document/d/1FZAOpi4hl6U8g-0txM5l65wOkNrPYcLzCpK3pL-Dv0E/edit?usp=sharing)
 - [CB Doc chat](https://docs.google.com/document/d/1N0oHC3sZXn_tffDy3XpENkDFoIA3bt5vUJ2w9QchLSs/edit?usp=drive_link)
 - [CB Architect chat](https://docs.google.com/document/d/1jpr79XrbtnHQ6MaP_V3OcMoBLDsj2KFU1LkGTH8KtSs/edit?usp=drive_link)
 - [Custom data set processing](https://docs.google.com/document/d/14zG_NXUELs4A2x4kHxsDFzCsTWG2VNV2rSnQF8Z0oDs/edit?usp=drive_link)
 - [Fine tuning local llms](https://docs.google.com/document/d/1nyDkyD2N16UMmGjLXumqXacWZZkNDi_h0Wh1lpJvmoA/edit?usp=drive_link)
 - [Hybrid search](https://docs.google.com/document/d/1PBQ28B5bk6UEozo7RF0vpNphluu2D92v0kxuO5wOz9c/edit?usp=drive_link)
 - [Retrieval Augmented Generation](https://docs.google.com/document/d/1dGrhkSQYk2pKX9-AojdJgPQ0fFMY3GkGK0oFbWgq43E/edit?usp=sharing)




## Confluence pages

 - [CBAAP Confluence](https://couchbasecloud.atlassian.net/wiki/spaces/QA/pages/2179793032/CBAAP+-+Couchbase+AI+App+Playground+-+Intern+Project)





## Installation

### Pre requisites

In a nutshell, we use Large Language Models to get the response given a proper prompt as input which contains the user query along with the context and the history if required. And there are several ways you can interact with the llms. We went through those wide range of options and came to a conclusion that, the framework "ollama" is very fast and efficient to interact with the llms. 
On a interesting note, we only use local llms (so we can make sure the data is secure) and ollama offers support to convert any local llm into a ollama model.
So throughout this entire application, we used ollama for AI responses and make sure you have ollama installed before moving on with the CBAAP installation.

To know more about [ollama](https://docs.google.com/document/d/1FZAOpi4hl6U8g-0txM5l65wOkNrPYcLzCpK3pL-Dv0E/edit?usp=sharing).

- Download and install the ollama framework from their official website and follow the steps.

```bash
  https://ollama.com/download
```

- Launch the ollama application.


- Install homebrew from their website
   https://brew.sh/

This repo is designed for Apple Silicon architecture. If your architecture is different, we kindly request you to hold and we will be lauching the CBAAP versions for other architectures soon.


### CBAAP Installation


- Clone this repository.
```bash
   git clone https://github.com/QEinterns/CBAAP-local-package.git
```
- Navigate into the cloned repo and make sure you are inside the CBAAP-local-package directory.

- There are two scripts (install.sh and run.sh) in this repo.\
   The install.sh downloads and installs all the necessary modules required for the CBAAP to run.\
   On successfull execution of install.sh, you have this run.sh script to run the application.

   Note: All the installations are done in a specific python virtual environment "cbaap_env".

   Before running these scripts, give the permissions using the below command.
```bash
   chmod +x install.sh
   chmod +x run.sh
```
- Now lets install all the necessary packages necessary for CBAAP by executing the install.sh script.
```bash
   ./install.sh
```
- Now that, all the necessary packages are installed and the ollama running in the background, lets start the application.

   Note: During the first app run, it might take longer time to initialize. Also the downloads are one time process. During the first run of imagine, a 10gb model file will get downloaded (if you are running proteus).
```bash
   ./run.sh
```

- Now visit localhost:5100 to access CBAAP in your web browser.
```bash
    http://localhost:5100/
```



## Authors

- [@Ashok Kumar Alluri](ashokkumar.alluri@couchbase.com)
- [@Nishanth VM](nishath.vm@couchbase.com)
- [@Sanjivani Patra](sanjivani.patra@couchbase.com)

import requests
import json
import PyPDF2

"This is pdf operation class contain all manipulation functions"
class pdf_operations:
    '''
    Some common functions for server interaction
    '''
    # Authentication API function
    def auth(self):
        '''Authenticates with the iLovePDF API and retrieves a token
        Returns:
            str: The authentication token for accessing the API'''
        url = "https://api.ilovepdf.com/v1/auth"
        payload = json.dumps({
            "public_key": "project_public_ddd44a9a1054084f86f7c089b57c0e9a_Pporqcfa3a8514b8e6495c4c92b74816933ed"
        })
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        token1 = (json.loads(response.text)['token'])
        return token1

     
    # Tool api function
    def start(self, token1, tool):
        '''Start a PDF manipulation task using the iLovePDF API
        Args:
            token1 : The authentication token obtained after authentication.
            tool : Name of the PDF manipulation tool to use
        Returns:
            task ID, server URL, and the bearer token used in the request'''
        
        url = f"https://api.ilovepdf.com/v1/start/{tool}"
        files = {}
        payload = {}
        bearer = f'Bearer {token1}'
        headers1 = {
            'Authorization': bearer,
        }

        response = requests.request(
            "GET", url, headers=headers1,   data=payload, files=files)
        res = json.loads(response.text)
        task, server = (res['task']), (res['server'])
        return task, server, bearer


    # Upload API
    def upload(self, server, bearer, payload, files):  
        '''Upload files to the iLovePDF server
            Args:
                server: The server URL where the upload should take place.
                bearer: The bearer token for authorization.
                payload (dict): The payload data for the upload request.
                files : List of files to be uploaded.
            Returns:
                list: A list of dictionaries containing server filenames and original filenames'''
        url = f"https://{server}/v1/upload"
        header = {
            'Authorization': bearer
        }
        lst = []
        for file in files:
            response = requests.request(
                "POST", url, headers=header, data=payload, files=[file])
            server_filename = json.loads(response.text)["server_filename"]
            lst.append({"server_filename": server_filename,
                        "filename": file[1][0]})
        return lst


    # process api
    def process(self, server, bearer, payload_1):
        '''Initiate a PDF processing task on the iLovePDF server
            Args:
                server: The server URL where the processing task should be initiated,
                bearer: The bearer token for authorization,
                payload_1: The payload data for the processing request,
            Returns:
                None: The function does not return a value, but initiates the PDF processing task'''
                                                                                     
        url = f"https://{server}/v1/process"
        headers = {'Content-Type': 'application/json',
                   'Authorization': bearer, }
        response = requests.request("POST", url, headers=headers, data=payload_1)
    

    # download api link
    def down(self, server, task, bearer, tool):
        '''Download the processed PDF from the iLovePDF server.
            Args:
                server: The server URL from which to download the PDF.
                task: The task ID for the specific processing task.
                bearer: The bearer token for authorization.
                tool: The name for the manipulated PDF.
            Returns:
                None: The function downloads and saves the PDF but doesn't return a value'''
        url = f"https://{server}/v1/download/{task}"
        payload = ""
        headers = {
            'Authorization': bearer
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            # Specify the file name and path where you want to save the PDF
            pdf_filename = f'{tool}downloaded_pdf.pdf'

            # Open the file in binary write mode ('wb') and write the   response content into it
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f'PDF saved as {pdf_filename}')


    '''
    Some function works on required feature
    '''
    # merge function
    def merge(self):
        '''Merges two pdf file into one pdf file
            Hilights:
                goes through all above functions
            return:none'''
        # Calling Auth fuction
        token = self.auth()
        # calling start function
        task, server, bearer = self.start(token, "merge")
        # local files
        files = [
            ('file', ('p.pdf', open('p.pdf', 'rb'), 'application/pdf')),
            ('file', ('html.pdf', open('html.pdf', 'rb'), 'application/pdf'))
        ]
        payload_0 = {
            "task": task,
            "tool": "merge"
        }
        # calling upload function
        lst = self.upload(server, bearer, payload_0, files)
        payload_1 = json.dumps({
            "task": task,
            "tool": "merge",
            "files": lst
        })
        # calling process function
        self.process(server, bearer, payload_1)
        # calling down function
        self.down(server, task, bearer, "merge")

    # split function
    def split(self):
        '''
        Spilits a pdf into two parts according to given range
          return:none
        '''
         # calling auth func
        token = self.auth()
         # calling start func
        task, server, bearer = self.start(token, "split")
        payload = {
            "task": task
        }
        # local file
        files = [
            ('file', ('html.pdf', open('html.pdf', 'rb'), 'application/pdf')),
        ]
         # calling upload func
        lst = self.upload(server, bearer, payload, files)
        payload = json.dumps({
            "task": task,
            "tool": "split",
            "ranges": "3-8",
            "files": lst
        })
        # calling process func
        self.process(server, bearer, payload)
        # calling down func
        self.down(server, task, bearer, "split")

    # unlock pdf
    def unlock(self):
        '''Unlocks pdf with password
            return:none'''
         # calling auth func
        token = self.auth()
         # calling start func
        task, server, bearer = self.start(token, "unlock")
        payload = {
            "task": task
        }
        # local file
        files = [
            ('file', ('JAICV2_protected.pdf', open(
                'D:\Assignment\JAICV2_protected.pdf', 'rb'), 'application/pdf'))
        ]
         # calling upload func
        lst = self.upload(server, bearer, payload, files)
        lst[0]["password"] = "Jj@1"
        payload = json.dumps({
            "task": task,
            "tool": "unlock",
            "files": lst,
        })
         # calling process func
        self.process(server, bearer, payload)
         # calling down func
        self.down(server, task, bearer, "unlock")


    # image to pdf
    def img_to_pdf(self):
        '''Converts image into pdf file
            return:none'''
         # calling auth func
        token = self.auth()
         # calling start func
        task, server, bearer = self.start(token, "imagepdf")
        payload = {
            "task": task
        }
        # local file
        files = [
            ('file',('ducati.jpg',open('D:\Assignment\ducati.jpg','rb'),'image/jpeg'))
        ]
         # calling upload func
        lst = self.upload(server, bearer, payload, files)
        payload = json.dumps({
            "task": task,
            "tool": "imagepdf",
            "files": lst,
        })
         # calling auth func
        self.process(server, bearer, payload)
         # calling auth func 
        self.down(server, task, bearer, "image_to_pdf")
        
        '''
            NOT WORKING CODE
                            '''
        
    # convert pdf
    def convert(self):
        token = self.auth()
        task, server, bearer = self.start(token, "pdfoffice")
        payload = {
            "task": task
        }
        files = [
            ('file', ('JAICV2.pdf', open(
                'C:/Users/91798/Downloads/JAICV2.pdf', 'rb'), 'application/pdf'))
        ]
        lst = self.upload(server, bearer, payload, files)
        lst[0]["convert_to"] = "docx"
        import pdb
        pdb.set_trace()
        payload = json.dumps({
            "task": task,
            "tool": "pdfoffice",
            "files": lst,
        })
        self.process(server, bearer, payload)
        self.down(server, task, bearer, "pdf_to_office")

    '''
            NOT WORKING CODE
                            '''

    # convert pdf to txt direct
    # Open the PDF file in read-binary mode
    def pdf_to_txt(self):
        with open('C:/Users/91798/Downloads/JAICV2.pdf', 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Initialize a variable to store the    extracted text
            extracted_text = ''

            # Loop through each page in the PDF
            for page_number in range(pdf_reader.numPages):
                # Get the text content of the page
                page = pdf_reader.getPage(page_number)
                page_text = page.extractText()

                # Append the text from the current  page to the extracted_text variable
                extracted_text += page_text
        # Print or save the extracted text as needed
        print(extracted_text)

'''Object of pdf_operation class'''
obj = pdf_operations()
# calling merge function from class
obj.merge()
# calling split function from class
obj.split()
# calling unlock function from class
obj.unlock()
# calling img_to_pdf function from class
obj.img_to_pdf()
'''NOT WORKING'''
# obj.convert()
# obj.pdf_to_txt()
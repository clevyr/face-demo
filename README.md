# face-demo
One-shot face identification

To run
`docker-compose up`

webapp is served at localhost:5001

Employee target images are located in `data/faces`

If you add/edit/delete an employee image, delete your `server/names_and_features.p` file.  The file will be re-generated on demand (which may take awhile if you have lots of employee photos).
Employee target files must follow the naming convention: 'firstname-lastname-smile.jpg'.

const http = require("http");
const request = require("request");
const cheerio = require("cheerio");
const path = require("path");
const fs = require("fs");
var site = "";

request("https://en.wikipedia.org/wiki/April_17", (error, response, html) => {
    if(!error && response.statusCode == 200){
        const $ = cheerio.load(html);
        site = $(".toc").next().next().text();
        //console.log(site.toString());
    }
});
fs.writeFile(path.join(__dirname, '','output.txt'), err =>{
    if (err) throw err;
    console.log(site);
});

const server = http.createServer((req, res) => {
    if (req.url === '/') {
        fs.readFile(
            path.join(__dirname,'' ,'main.html'), (err, content) => {
                if (err) throw err;
                res.writeHead(200, {'Content-type' : 'text/html'})
                res.write(content);
                console.log("sent");
                res.end();
            }
        );
    }else if (/\.(css)$/.test(req.url)){
        res.writeHead(200, {'Content-Type': 'text/css'});
        res.write(fs.readFileSync(__dirname + req.url, 'utf8')); // <--- add this line
        res.end();
    }else if (/\.(js)$/.test(req.url)){
        res.writeHead(200, {'Content-Type': 'text/javascript'});
        res.write(fs.readFileSync(__dirname + req.url, 'utf8')); // <--- add this line
        res.end();
    }else{
        res.end();
    }
});

const PORT = 7000;
server.listen(PORT, () => console.log("req has happened"));



//Usage: node solve.js
function findVariants(targetChar) {
    let targetHost = 'fake' + targetChar + '.com';
    for (i = 32; i <= 65535; i++) {
        let candidateChar = String.fromCharCode(i);
        let input = 'http://fake' + candidateChar + '.com';
        try {
            let url = new URL(input);
            if (url.hostname === targetHost) {
                console.log(targetChar, ':', i, candidateChar);
            }
        }
        catch(e) {
        }
    }
}
// Target domain name
let domain = 'the.c0o0o0l-fl444g.server.internal';
let domainSet = new Set(domain);
for (c of domainSet) {
    findVariants(c)
}
var ghpages = require('gh-pages');

ghpages.publish(
    'public',
    {
        branch: 'gh-pages',
        repo: 'https://github.com/lobziq/pdmafiadatabase.git',
        user: {
            name: 'lobziq',
            email: 'lobziq@gmail.com'
        }
    },
    () => {
        console.log('Deploy Complete!')
    }
)
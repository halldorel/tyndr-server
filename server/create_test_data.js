var app = require('./server');
var dataSource = app.dataSources.tyndr;
var Advert = app.models.advert;
var adverts = [ 
    {
        name: "Pulsa",
        lost: true,
        resolved: false,
        location: "64.13548,-21.89541",
        description: "Frekar ljótt dýr",
        reward: "500",
        created_at: new Date()
    },
    {
        name: "Trefill",
        lost: true,
        resolved: false,
        location: "64.13548,-21.89541",
        description: "Holdsveikt dýr",
        reward: "1500",
        created_at: new Date()
    },
    {
        name: "Salmonella",
        lost: true,
        resolved: false,
        location: "64.13548,-21.89541",
        description: "Mjög krúttleg",
        reward: "200",
        created_at: new Date()
    }
];

var count = adverts.length;
dataSource.automigrate('advert', function (err)
{
    adverts.forEach(function(ad)
    {
        Advert.create(ad, function(err, result)
        {
            if(!err)
            {
                console.log('Record created:', result);
                count--;
                if(count === 0)
                {
                    console.log('done');
                    dataSource.disconnect();
                }
            }
        });
    });
});
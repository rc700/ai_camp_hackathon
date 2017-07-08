// dependencies
var restify = require('restify');
var builder = require('botbuilder');
var axios = require('axios');

// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function () {
   console.log('%s listening to %s', server.name, server.url); 
});

// Create chat connector for communicating with the Bot Framework Service
var connector = new builder.ChatConnector({
    appId: process.env.MICROSOFT_APP_ID,
    appPassword: process.env.MICROSOFT_APP_PASSWORD
});

// create the bot
var bot = new builder.UniversalBot(connector);

// Listen for messages from users 
server.post('/hack', connector.listen());

// This bot enables users to either make a dinner reservation or order dinner.
var bot = new builder.UniversalBot(connector, function(session){
	session.send("Welcome to PREDICT MY IT FUTURE")
    var msg = "Want to find out your CAREER IN IT?";
    session.send(msg);
});

// Dinner menu
var dinnerMenu = {
    "Potato salad - $5.99":{
        Description: "Salad",
        Price: 5.99
    },
    "Tuna sandwich - $6.89":{
        Description: "Sticky toffee pudding",
        Price: 6.89
    },
    "Clam Chowder - $4.50":{
        Description: "Malteaser cheesecake",
        Price: 4.50
    }
};

// Help
bot.dialog('help', function(session){
    // Send message
    session.endDialog('To talk with the bot say Hello');
}).triggerAction({
    matches : /^help$/,
    onSelectAction: (session, args, next) => {
        session.beginDialog(args.action, args);
    }
});

// Dinner reservation
bot.dialog('dinner reservation', [function(session){
    // Send message
    session.send('Let us make a dinner reservation');
    session.beginDialog("askForDateTime")
    
},
function (session, results){
session.dialogData.reservationDate = builder.EntityRecognizer.resolveTime([results.response]);
session.beginDialog("askForPartySize")
},
function (session, results){
    if(results.response){
        session.dialogData.partySize = results.response
    }
    session.beginDialog("askForReserverName")
},
function (session, results){
    if(results.response){
        session.dialogData.reserverName = results.response
        session.send("Please confirm your booking details:<br/><br/>Date: %s <br/>Party size: %s <br/>ReserverName: %s",
        session.dialogData.reservationDate, session.dialogData.partySize, session.dialogData.reserverName)

        endDialog();
    }
}

]).triggerAction({
    matches : /^dinner reservation$/
})

// Gets date
bot.dialog("askForDateTime",[
    function(session){
        builder.Prompts.time(session, "Please provide a reservation time - i.e. \"June 6th at 4pm\"")
    },
    function (session, results){
        session.endDialogWithResult(results)
    }
])

// Gets party size
bot.dialog("askForPartySize",[
    function(session){
        builder.Prompts.text(session, "What is the party size?")
    },
    function (session, results){
        session.endDialogWithResult(results)
    }
])

// Get reserver name
bot.dialog("askForReserverName",[
    function(session){
        builder.Prompts.text(session, "What is your name?")
    },
    function (session, results){
        session.endDialogWithResult(results)
    }
])

// Get country
bot.dialog('get country', [
    function(session){
        session.send("Let\'s get started!");
		builder.Prompts.text(session, "What country are you from?")
        //builder.Prompts.choice(session, "Dinner Menu!", dinnerMenu)
		//builder.Prompts.choice(session, "What country are you from?", ['UK', 'USA'])
    },
    function(session, results){
        if(results.response){
			var msg = session.dialogData.Country = results.response;
			session.send("You are from " + msg)

            //builder.Prompts.text(session, "What is your formal education?")
			session.send("What is your formal education?")
			var msg = new builder.Message()
                .addAttachment({ 
                    //text: 'PHD',
                    actions: [ { title: 'PHD', message: 'PHD' }]
                 })
                .addAttachment({ 
                    //text: 'Master\'s',
                    actions: [ { title: 'Masters', message: 'Masters' }]
                 })
                .addAttachment({ 
                    //text: 'Bachelor\'s',
                    actions: [ { title: 'Bachelor\'s', message: 'Bachelors' }]
                 })
				 .addAttachment({ 
                    //text: 'Secondary school',
                    actions: [ { title: 'Secondary school', message: 'Secondary school' }]
                 })
				 .addAttachment({ 
                    //text: 'Primary/Elementary school',
                    actions: [ { title: 'Primary/Elementary school', message: 'Primary/Elementary school' }]
                 });
            builder.Prompts.choice(session, msg, "PHD|Masters|Bachelors|Secondary school|Primary/Elementary school");
        }
    },

	function(session, results){
			if(results.response){
				var msg = session.dialogData.FormalEducation = results.response;
				session.send("Your formal education is: " + session.dialogData.FormalEducation.entity)
				
				session.send("Would you rather work at home or remotely?")
				var msg = new builder.Message()
                .addAttachment({ 
                    actions: [ { title: 'Computer Science/Software Engineering', message: 'Computer Science/Software Engineering' }]
                 })
                .addAttachment({ 
                    actions: [ { title: 'Computer related discipline', message: 'Computer related discipline' }]
                 })
                .addAttachment({ 
                    actions: [ { title: 'Science related discipline', message: 'Science related discipline' }]
                 })
				 .addAttachment({ 
                    actions: [ { title: 'Other', message: 'Other' }]
                 });
            builder.Prompts.choice(session, msg, "Computer Science/Software Engineering|Computer related discipline|Science related discipline|Other");
			}
		},

	function(session, results){
			if(results.response){
				var msg = session.dialogData.MajorUndergrad = results.response;
				session.send("Your major undergrad is: " + session.dialogData.MajorUndergrad.entity)

				//builder.Prompts.text(session, "Would you rather work at home or remotely?")
				session.send("Would you rather work at home or remotely?")
				var msg = new builder.Message()
                .addAttachment({ 
                    //text: 'All or most of the time',
                    thumbnailUrl: 'https://image.flaticon.com/icons/svg/201/201623.svg',
                    actions: [ { title: 'All or most of the time', message: 'All or most of the time' }]
                 })
                .addAttachment({ 
                    //text: 'Half the time',
                    thumbnailUrl: 'https://image.flaticon.com/icons/svg/252/252026.svg',
                    actions: [ { title: 'Half the time', message: 'Half the time' }]
                 })
                .addAttachment({ 
                    //text: 'A few days each month',
                    thumbnailUrl: 'https://image.flaticon.com/icons/svg/360/360861.svg',
                    actions: [ { title: 'A few days each month', message: 'A few days each month' }]
                 })
				 .addAttachment({ 
                    //text: 'Never',
                    thumbnailUrl: 'https://image.flaticon.com/icons/svg/147/147040.svg',
                    actions: [ { title: 'Never', message: 'Never' }]
                 });
            builder.Prompts.choice(session, msg, "All or most of the time|Half the time|A few days each month|Never");
			}
		},

	function(session, results){
			if(results.response){
				var msg = session.dialogData.homeRemote = results.response;
				session.send("You prefer : " + session.dialogData.homeRemote.entity)

				builder.Prompts.text(session, "How many years of programming experience do you have? (not including industry)")
			}
		},

	function(session, results){
			if(results.response){
				var msg = session.dialogData.YearsProgram = results.response;
				session.send("You have " + msg + " years of programming experience")

				builder.Prompts.text(session, "How many years of professional programming experience do you have?")
			}
		},

    function(session, results){
        if(results.response){
            session.dialogData.YearsCodedJob = results.response;
            var msg = "You have #%s years of professional programming experience";
			session.send(session.dialogData.Country)
			session.send(session.dialogData.FormalEducation.entity)
			session.send(session.dialogData.MajorUndergrad.entity)
			session.send(session.dialogData.homeRemote.entity)
			session.send(session.dialogData.YearsProgram)
			session.send(session.dialogData.YearsCodedJob)
			
			var userHomeRemote = session.dialogData.homeRemote.entity
			var userMajorUndergrad = session.dialogData.MajorUndergrad.entity
			var userFormalEducation = session.dialogData.FormalEducation.entity

			// Formal education
			switch(session.dialogData.FormalEducation.entity){
				case "PHD":
				userFormalEducation = 4
				break;
				case "Masters":
				userFormalEducation = 3
				break;
				case "Bachelors":
				userFormalEducation = 2
				break;
				case "Secondary school":
				userFormalEducation = 1
				break;
				case "Primark/Elementary school":
				userFormalEducation = 0
				break;
			}

			switch(session.dialogData.MajorUndergrad.entity){
				case "Computer Science/Software Engineering":
				userMajorUndergrad = 3
				break;
				case "Computer related discipline":
				userMajorUndergrad = 2
				break;
				case "Science related discipline":
				userMajorUndergrad = 1
				break;
				case "Other":
				userMajorUndergrad = 0
				break;
			}
			
			switch(session.dialogData.homeRemote.entity){
				case "Never":
				userHomeRemote = 3
				break;
				case "Half the time":
				userHomeRemote = 2
				break;
				case "A few days each month":
				userHomeRemote = 1
				break;
				case "All or most of the time":
				userHomeRemote = 0
				break;
			}

			// Formaleducation, majorUndergrad, home/remote, yearsprog, industryears, "country (uk)"
			userInputs = [userFormalEducation, userMajorUndergrad, userHomeRemote, YearsProgram, YearsCodedJob,4]
			// GET PREDICTION & OUTPUT IT

			//list might have to be json object
			//axios.post('localhost:1234/predict',list)




			var msg = new builder.Message(session);
			msg.attachmentLayout(builder.AttachmentLayout.carousel)
			msg.attachments([
				new builder.HeroCard(session)
					.title("sweet doggo")
					.subtitle("she loves grass")
					.text("too precious for this world")
					.images([builder.CardImage.create(session, 'https://media.giphy.com/media/Z3aQVJ78mmLyo/giphy-downsized-large.gif')])
					.buttons([
						builder.CardAction.imBack(session, "buy classic white t-shirt", "Click for more doggos")
					]),
				new builder.HeroCard(session)
					.title("merry christmas")
					.subtitle("*tap tap*")
					.text("legend says he's still tapping")
					.images([builder.CardImage.create(session, 'https://38.media.tumblr.com/c74bd4d45fd0e61501a6aec327030035/tumblr_inline_nztaicNC111rbhfb4_500.gif')])
					.buttons([
					builder.CardAction.openUrl(session, 'https://www.google.co.uk/search?q=doggo+gif&client=ubuntu&hs=2aT&channel=fs&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiIt-vAsvLUAhUiJMAKHcwwCH0Q_AUICigB&biw=928&bih=957#imgrc=bEK1hXGjrqsHzM:', 'Take me on an adventure')
					])
			]);
            session.endConversation(msg, session.dialogData.YearsCodedJob)
        }
    } 

]).triggerAction({
    matches : /^yes$|^ok$|^okay$|^yeah$|^yas$|^aye$/i,
})
.endConversationAction(
    "endOrderDinner", "Ok, goodbye.",
    {
        matches: /^cancel$|^goodbye$/i,
        confirmPrompt: "This will cancel your order. Are you sure?"
    }
)
// dependencies
var restify = require('restify');
var builder = require('botbuilder');

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

// Order dinner
bot.dialog('order dinner', [
    function(session){
        session.send("Let\'s order dinner");
        builder.Prompts.choice(session, "Dinner Menu!", dinnerMenu)
    },
    function(session, results){
        if(results.response){
            var order = dinnerMenu[results.response.entity];
            var msg = "You have ordered: %(Description)s for the glorious price of $%(Price)f."
            
            if(order.Description == "Salad"){
                session.send("you have a problem.")
            }
            
            session.send("Solid choice.")
            session.dialogData.order = order;
            session.send(msg, order)
            builder.Prompts.text(session, "What is your room number?")
        }
    },

    function(session, results){
        if(results.response){
            session.dialogData.room = results.response;
            var msg = "Thank you. Your order will be delivered to room #%s";
            session.endConversation(msg, session.dialogData.room)
        }
    } 

]).triggerAction({
    matches : /^order dinner$/,
})
.endConversationAction(
    "endOrderDinner", "Ok, goodbye.",
    {
        matches: /^cancel$|^goodbye$/i,
        confirmPrompt: "This will cancel your order. Are you sure?"
    }
)

// Get country
bot.dialog('get country', [
    function(session){
        session.send("Let\'s get started!");
		builder.Prompts.text(session, "What country are you from?")
        //builder.Prompts.choice(session, "Dinner Menu!", dinnerMenu)
    },
    function(session, results){
        if(results.response){
			var msg = session.dialogData.Country = results.response;
			session.send("You are from " + msg)

            builder.Prompts.text(session, "What is your formal education?")
        }
    },

	function(session, results){
			if(results.response){
				var msg = session.dialogData.FormalEducation = results.response;
				session.send("Your formal education is: " + msg)

				builder.Prompts.text(session, "What is your major undergrad?")
			}
		},

	function(session, results){
			if(results.response){
				var msg = session.dialogData.MajorUndergrad = results.response;
				session.send("Your major undergrad is: " + msg)

				builder.Prompts.text(session, "Would you rather work at home or remotely?")
			}
		},

	function(session, results){
			if(results.response){
				var msg = session.dialogData.homeRemote = results.response;
				session.send("You prefer : " + msg)

				builder.Prompts.text(session, "How many years of programming experience do you have? (non-professional)")
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
			session.send("testtttt" + session.dialogData.homeRemote)
			// GET PREDICTION & OUTPUT IT
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
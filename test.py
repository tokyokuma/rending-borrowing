    '''
    if '登録' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録したいのは何人？')
         )
         if event.message.text.isdigit():
             num_of_members = event.message.text
             member_names = []
             for i in range(0, num_of_people):
                 line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='str(num_of_people[i] + 1)'+'目の名前は？')
                 )
                 name[i] = event.message.text

         else:
             line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='数字のみを入力してくだい？')
             )

    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='「' + event.message.text + '」って何？')
         )
    '''

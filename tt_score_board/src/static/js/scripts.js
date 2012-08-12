scoreFeeder={
		__init__:function(){
			
			

			$(document).ready(function()
			{
			$("div.n").live("click", function()
				{
				var tr=$(this).attr("id");
				 $("#tr").animate({fontSize:"1.5em"},"slow");
			var data =$(this).find(".score").html();
			        $(this).find(".score").html(data+1);
				$.ajax({
			  		type: "POST",
			  		url: "",
			  		data: { 'updateString':tr?(tr+"+"):""},
					dataType:"json",
					success: function(msg)
						{
						console.log(msg)
						renderScore.updatePage(msg)
						}
					
					})
				}
				);
			}
			);


		}
		
		
}


renderScore={
		updateOnInTerval:function(){
			var int=self.setInterval(function(){getScore()},5000);

			
		},
		getScore:function(){
			$.ajax({
		  		type: "get",
		  		url: "",
		  		data: { },
				dataType:"json",
				success: function(msg)
					{
					console.log(msg)
					renderScore.updatePage(msg)
					}
				
				})
		},
		
		updatePage:function(msg){
			

			msg['teams'][1]
			msg['teams'][2]
			
			$('#A .score').html(msg['teams'][0]['Team_A_score'])
			$('#A1 .score').html(msg['teams'][0]['playersPerformances']['A1_score'])
			$('#A2 .score').html(msg['teams'][0]['playersPerformances']['A2_score'])
			$('#B1 .score').html(msg['teams'][1]['playersPerformances']['B1_score'])
			$('#B2 .score').html(msg['teams'][1]['playersPerformances']['B2_score'])
			$('#B .score').html(msg['teams'][1]['Team_B_score'])
			
			if (msg['teams'][0]['players'][1] == 'A1' &&  $('#A2').css("top") == "0px")
				
				{ 
					$('#A1').css("top","0")

					$('#A2').css("top","50%")					
				}
				
			

			if (msg['teams'][1]['players'][1] == 'B1' && $('#B2').css("top") != "0px" )
				{ 
					$('.players .n#B2').css("top","0%")
					
					$('.players .n#B1').css("top","50%")					
				}
			
			if (msg['teams'][0]['players'][0] == 'A1' &&  $('#A1').css("top") == "0px")
				
				{ 
					$('#A2').css("top","0px")

					$('#A1').css("top","50%")					
				}
				
			

			if (msg['teams'][1]['players'][0] == 'B1' && $('#B1').css("top") != "0px" )
				{ 
					$('.players .n#B2').css("top","50%")
					
					$('.players .n#B1').css("top","0px")					
				}
		
			if (msg['teams'][0]['Team_A_score']==21)
				{
				$('#A .rslt').html("Win")
				}
			if (msg['teams'][1]['Team_B_score']==21)
				{
				$('#B .rslt').html("Win")
				}
			if (msg['teams'][0]['currentServing'])
			
				{
				$('#A .serve').html("Serving")	
				}
			else
				{
				$('#A .serve').html("")
				}
			if (msg['teams'][1]['currentServing'])
			
				{
				$('#B .serve').html("Serving")	
				}
       			else	
				{
				$('#B .serve').html("")
				}

			if(msg['teams'][0]['advantage'])
				{
                                $('#A .adv').html("adv")
				}
			else
				{
				$('#A .adv').html("")
				}
			
			if(msg['teams'][1]['advantage'])
				{
                                $('#B .adv').html("adv")
				}
			else
				{
				$('#B .adv').html("")
				}
			if(msg['teams'][0]['win'])
				{
                                $('#A .win').html("Win")
				}
			else
				{
				$('#A .win').html("")
				}
			if(msg['teams'][1]['win'])
				{
                                $('#B .win').html("win")
				}
			else
				{
				$('#B .win').html("")
				}

		}
		
		
}
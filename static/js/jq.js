$(document).ready(function(){

	function getCookie(name) {
			  var cookieValue = null;
			  if (document.cookie && document.cookie != '') {
					var cookies = document.cookie.split(';');
			  for (var i = 0; i < cookies.length; i++) {
				   var cookie = jQuery.trim(cookies[i]);
			  if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				  break;
				 }
			  }
		  }
	 return cookieValue;
	}
    
	var csrftoken = getCookie('csrftoken');

    function validate() {
        var a = true;
        if ($('#text1').val() == '' ) {
            $('#text1').css('border-color', 'red');
            $('#text1').css('border-width', '3px');
            a = false
        }
        if ($('#key').val() == '') {
            $('#key').css('border-color', 'red');
            $('#key').css('border-width', '3px');
            a = false
        }
        return a
    }
    
    function clear_validation() {
        $('#text1').css({'border-color': '#CCCCCC', 'border-width': '1px'});
        $('#key').css({'border-color': '#CCCCCC', 'border-width': '1px'});
    }
    
	$('#enc').click(encrypt);
	function encrypt() {
	    if (validate() == true){
	        clear_validation();
	        $.ajax({
            type: "POST",
            url: "/encrypt/",
            data: {
                "text": $("#text1").val(),
                "key": $("#key").val(),
                "csrfmiddlewaretoken": csrftoken
            },
				dataType: "json",
				cache: false,
				success: function(result){
                    $("#text2").val(result['finaltext']);
				}
		   });
        }

    }

	$('#dec').click(decrypt);
	function decrypt() {
	    if (validate() == true){
	        clear_validation();
            $.ajax({
            type: "POST",
            url: "/decrypt/",
            data:{
                "csrfmiddlewaretoken" : csrftoken,
                "text": $("#text1").val(),
                "key": $("#key").val()
            },
            dataType: "json",
            cache: false,
            success: function(result){
                $("#text2").val(result['finaltext']);
            }});
	    }
    }

    $('#text1').change(function() {

        var mytext = $('#text1').val().toLowerCase();
        var i;
        var data = new Array();
        var mymap = new Map();
        var maparr = new Array();
        for(i=0;i<mytext.length;i++)
        {
            if (mymap.has(mytext[i]))          //проверка на входимость символа в Мар
            {
                mymap.set(mytext[i], mymap.get(mytext[i])+1);   //подсчет букв в строке с помощью 
            }													// Map
            else{
                if (mytext[i] != ' ')                         //Чтобы не подсчитывал пробелы
                {
                    mymap.set(mytext[i],1);
                    maparr.push(mytext[i]);
                }

            }
        }
        maparr.sort(); 								//сортируем в алфавит порядке
        for(i = 0;i < maparr.length;i++)
        {
            data.push(new Array(maparr[i],mymap.get(maparr[i])));       //добавляем в нужном виде на диаграмму
        }

		$.plot("#placeholder", [ data ], {
			series: {
				bars: {
					show: true,
					barWidth: 0.6,
					align: "center"
				}
			},
			xaxis: {
				mode: "categories",
				tickLength: 0
			}
		});

		$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");

        $.ajax({
        type: "POST",
        url: "/find/",
        data:{
            "csrfmiddlewaretoken" : csrftoken,
            "mytext": $("#text1").val()
        },
        dataType: "json",
        cache: false,
        success: function(result){
            if (result['enc']=='false')
            {
                $(".to_guess").html('Данный текст не является зашифрованным.');
            }
            else if (result['enc']=='true')
            {
                $(".to_guess").html('Данный текст зашифрован.\nЗашифрованное слово: '+result['word']+'. Ключ = '+ result['key']);
            }
            else
            {
                $(".to_guess").html('К сожалению, невозможно определить.');
            }
        }});
	});
});



function get_query_value_by_key(key)
{
    var url = location.href;
    var address = url.split("?");
    var res = -1;
    
    if (address.length > 1)
    {
        var query_arr = address[1].split("&");
        for (var i = 0; i < query_arr.length; ++i)
        {
            var pair = query_arr[i].split("=");
            
            if (pair.length > 1 && pair[0] == key)
            {
                return pair[1];
            }
        }
    } 

    return -1;
}

function visualize(data)
{
    var current_page = get_query_value_by_key("page");
    var jsonfile = get_query_value_by_key("jsonfile");

    if (jsonfile == -1) jsonfile = "queries";
    if (current_page == -1) current_page = 1;
    if (jsonfile != "queries") jsonfile = "upload/" + jsonfile;

    for (var i = (current_page - 1) * 10; i < (current_page - 1) * 10 + 10 && i < data.length; ++i)
    {
        document.write("<tr style=\"height: 300px;\">");
        for(var j = 0; j < 4; ++j)
        {
            document.write("<td class=\"u-border-1 u-border-palette-5-dark-1 u-table-cell u-table-cell-1\">");
            if (j == 0)
            {
                document.write("Name: " + data[i][0] + ".mp4<br/>");
                document.write("&nbsp;<br/>");
                document.write("<video class=\"video\" src='/" + jsonfile + "/" + data[i][0] + ".mp4' controls></video>");
            }
            else 
            {
                document.write("Name: " + data[i][1][j-1][0] + ".mp4<br/>");
                document.write("Simularity: " + Math.round(data[i][1][j-1][1] * 100) / 100);
                document.write("<video class=\"video\" src='/database/" + data[i][1][j - 1][0] + ".mp4' controls></video>");
            }
            document.write("</td>");
        }
        document.write("</tr>");
    }
}

function select_json(data)
{
    document.write("<select onchange=\"this.options[this.selectedIndex].value && (window.location = this.options[this.selectedIndex].value);\">")
    
    document.write("<option value=\"\"></option>");

    for (var i = 0; i < data.length; ++i)
    {
       var address = location.href.split("?")[0];
       var current_page = get_query_value_by_key("page");
       if (current_page == -1) current_page = 1;
       document.write("<option value=\"" + address + "?" + "jsonfile=" + data[i] + "\">");
       document.write(data[i]);
       document.write("</option>");
    }
    document.write("</select>");
}

function write_foot(data)
{
    var current_page = get_query_value_by_key("page");
    var label = true;

    if (current_page == -1) current_page = 1;

    for (var i = 0; i < data.length / 10; ++i)
    {
        if (i + 1 == current_page)
        {
            document.write((i + 1) + "&nbsp;");
            label = true;
        }
        else if (i <= 2 || i > data.length / 10 - 3 || Math.abs((i + 1) - current_page ) < 3)
        {
            document.write("<a href=\"" + location.href.split("?")[0] + "?page=" + (i + 1) + "\">" + (i + 1) + "</a>");
            document.write("&nbsp;");
            label = true;
        }
        else if (label == true)
        {
            document.write("...&nbsp;");
            label = false;
        }
    }
}
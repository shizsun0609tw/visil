function visualize(data)
{
    var url = location.href;
    var address = url.split("?");
    var page = address[1].split("=")[1];

    for (i = (page - 1) * 10; i < (page - 1) * 10 + 10; ++i)
    {
        document.write("<tr style=\"height: 300px;\">");
        for(j = 0; j < 4; ++j)
        {
            document.write("<td class=\"u-border-1 u-border-palette-5-dark-1 u-table-cell u-table-cell-1\">");
            if (j == 0)
            {
                document.write("Name: " + data[i][0] + ".mp4<br/>");
                document.write("&nbsp;<br/>");
                document.write("<video class=\"video\" src='/queries/" + data[i][0] + ".mp4' controls></video>");
            }
            else 
            {
                document.write("Name: " + data[i][1][j-1][0] + ".mp4<br/>");
                document.write("Simularity: " + Math.round(data[i][1][j-1][1] * 100) / 100);
                document.write("<video class=\"video\" src='/database/" + data[i][1][j - 1][0] + ".mp4' controls></video>");
            }
            document.write("</td>");
        }
        document.write("</tr>")
    }
}

function write_foot(data)
{
    var url = location.href;
    var address = url.split("?");
    var current_page = address[1].split("=")[1];
    
    var label = true;
    for (i = 0; i < data.length / 10; ++i)
    {
        if (i + 1 == current_page)
        {
            document.write((i + 1) + "&nbsp;");
            label = true;
        }
        else if (i <= 2 || i > data.length / 10 - 3 || Math.abs((i + 1) - current_page ) < 3)
        {
            document.write("<a href=\"" + address[0] + "?page=" + (i + 1) + "\">" + (i + 1) + "</a>");
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
import xml.etree.ElementTree as ElTree
from chart import create_chart


def data_calculator(file_name):
    """
    :param file_name: Output.xml
    :return:
    """
    context = ElTree.iterparse(file_name)
    overall_result = dict()
    list_of_tags = []
    tag_results = {}

    for action, elem in context:
        if elem.tag == 'tag':
            list_of_tags.append(elem.text)
        if elem.tag == 'stat':
            try:
                if elem.text == 'All Tests':
                    overall_result['fail'] = elem.attrib['fail']
                    overall_result['pass'] = elem.attrib['pass']
                if elem.text in list_of_tags:
                    tag_results[elem.text] = {}
                    tag_results[elem.text]['fail'] = int(elem.attrib['fail'])
                    tag_results[elem.text]["pass"] = int(elem.attrib['pass'])

            except RuntimeError as e:
                print("OOPS" + str(e))
                continue

    return overall_result, tag_results


def robo_graph_generator():
    overall_result, tag_results = data_calculator('output.xml')
    total_pass = int(overall_result['pass'])
    total_fail = int(overall_result['fail'])
    total_result = total_pass + total_fail

    all_test_case_data = f"""\
        <div align="center" style="vertical-align:bottom">
            <div align="center" style="vertical-align:bottom">
                <table border="1" align="centre">
                    <tr bgcolor = 0CE36B align="center"><th>Total Test Cases</th><th>Passed</th><th>Failed</th></tr>
                    <tr><th>{total_result}</th><th>{total_pass}</th><th>{total_fail}</th></tr>
                </table>
            </div>
        </div>"""

    html_data = create_chart(overall_result, tag_results)
    html = f"""\
<html>
    <head>
        <meta charset="utf-8" />
    </head>
    <H1 align="center">Automation execution summary</H1>
    <body>
        <div>
{all_test_case_data}
        </div>
        <div>
{html_data}
        </div>
    </body>
</html>"""
    f = open("graph.html", 'w+')
    f.write(html)
    f.close()


if __name__ == "__main__":
    robo_graph_generator()

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using CodeMonkey.Utils;

public class Graph : MonoBehaviour
{
    [SerializeField]
    private Sprite circleSprite;
    [SerializeField]
    private Sprite lineSprite;
    private RectTransform graphContainer;
    private RectTransform labelTemplateX;
    private RectTransform labelTemplateY;
    private RectTransform dashTemplateX;
    private RectTransform dashTemplateY;
    private RectTransform Title;
    private RectTransform titlex;
    private RectTransform titley;
    //GameObject[] array1 = new GameObject[48];
    private List<GameObject> circle = new List<GameObject> { };
    private List<GameObject> connection = new List<GameObject> { };

    private void Awake()
    {
        // graphContainer = transform.Find("Graph").GetComponent<RectTransform>();
        

        graphContainer = transform.GetComponent<RectTransform>();
        labelTemplateX = transform.Find("LabelTemplateX").GetComponent<RectTransform>();
        labelTemplateY = transform.Find("LabelTemplateY").GetComponent<RectTransform>();
        dashTemplateX = transform.Find("dashTemplateX").GetComponent<RectTransform>();
        dashTemplateY = transform.Find("dashTemplateY").GetComponent<RectTransform>();
        Title = transform.Find("Title").GetComponent <RectTransform> ();
        titlex = transform.Find("titleX").GetComponent<RectTransform>();
        titley= transform.Find("titleY").GetComponent<RectTransform>();

        //CreateCircle(new Vector2(300, 510));
        // List<int> valueList = new List<int>() { 0, 200, 400, 600, 800, 1000, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000 };
        // List<string> stringList = new List<string>() { "A", "B", "C", "D", "E", "F", "G", "h", "i", "j", "k", "l", "m", "n", "o" };
        List<int> valueList = new List<int>() {  };
         List<string> stringList = new List<string>() {  };
        ShowGraph(valueList, stringList);
        
    }

    private GameObject CreateCircle(Vector2 anchoredPosition)
    {
       
        GameObject gameObject = new GameObject("circle", typeof(Image));
        gameObject.transform.SetParent(graphContainer, false);
        gameObject.GetComponent<Image>().sprite = circleSprite;
        RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
        rectTransform.anchoredPosition = anchoredPosition;
        rectTransform.sizeDelta = new Vector2(11, 11);
        rectTransform.anchorMin = new Vector2(0, 0);
        rectTransform.anchorMax = new Vector2(0, 0);
        return gameObject;

    }

  
    public void ShowGraph(List<int> valueList,List<string>stringList)
    {
       
        foreach (GameObject u in circle)
        {
            Destroy(u);

        }
        circle.Clear();
        foreach (GameObject u in connection)
        {
            Destroy(u);

        }
        connection.Clear();
        float graphHeight = graphContainer.sizeDelta.y;
        float yMaximum = 100f;
        float xSize = 950f;
        int nbvalues = valueList.Count;
       
        RectTransform titre = Instantiate(Title);
        titre.SetParent(graphContainer, false);
        titre.gameObject.SetActive(true);
        titre.anchoredPosition = new Vector2(475, 30);
        titre.GetComponent<Text>().text = "Measure of humidity soil";


        
        GameObject lastCircleGameObject = null;
        for (int i = 0; i < valueList.Count; i++)
        {
            float xPosition = (xSize / nbvalues) * i;//i * xSize + xSize;
            float yPosition = ((valueList[i] / yMaximum) * graphHeight);
            GameObject circleGameObject =  CreateCircle(new Vector2(xPosition, yPosition));

            circle.Add(circleGameObject);
          

            if (lastCircleGameObject != null)
            {
              GameObject connect= CreateDotConnection(lastCircleGameObject.GetComponent<RectTransform>().anchoredPosition, circleGameObject.GetComponent<RectTransform>().anchoredPosition);
                connection.Add(connect);
            }
            lastCircleGameObject = circleGameObject;

            RectTransform labelX = Instantiate(labelTemplateX);
            labelX.SetParent(graphContainer,false);
            labelX.gameObject.SetActive(true);
            labelX.anchoredPosition = new Vector2(xPosition, -50f);

            if (i % 8 == 0)
            {
                labelX.GetComponent<Text>().text = stringList[i];
            }
            else
            {
                labelX.GetComponent<Text>().text = "";
            }

            RectTransform dashY = Instantiate(dashTemplateY);
            dashY.SetParent(graphContainer,false);
            dashY.gameObject.SetActive(true);
            if (nbvalues > 15)
            {
                for (int j = 0; j < 15; j++)
                { 
                dashY.anchoredPosition = new Vector2(950f/15*j, 250);
                }
            }
            else { dashY.anchoredPosition = new Vector2(xPosition, 250); }
            
        }

        int separatorCount = 20;
        for (int i=0;i<=separatorCount;i++)
        {
            RectTransform labelY = Instantiate(labelTemplateY);
            labelY.SetParent(graphContainer,false);
            labelY.gameObject.SetActive(true);
            float normalizedValue = i * yMaximum / separatorCount;
            labelY.anchoredPosition = new Vector2(-40f,i*graphHeight/separatorCount);
            labelY.GetComponent<Text>().text = Mathf.RoundToInt(normalizedValue).ToString();

            //si veut quadriller en X
            RectTransform dashX = Instantiate(dashTemplateX);
            dashX.SetParent(graphContainer,false);
            dashX.gameObject.SetActive(true);
            dashX.anchoredPosition = new Vector2(475, i * graphHeight / separatorCount);
        }

        RectTransform titleX=Instantiate(titlex);
        titleX.SetParent(graphContainer, false);
        titleX.gameObject.SetActive(true);

        RectTransform titleY = Instantiate(titley);
        titleY.SetParent(graphContainer, false);
        titleY.gameObject.SetActive(true);

    }

    private GameObject CreateDotConnection(Vector2 dotPositionA, Vector2 dotPositionB)
    {
        GameObject gameObject = new GameObject("dotConnection", typeof(Image));
        gameObject.transform.SetParent(graphContainer, false);
        gameObject.GetComponent<Image>().sprite = lineSprite ;
        RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
        Vector2 dir = (dotPositionB - dotPositionA).normalized;
        float distance = Vector2.Distance(dotPositionA, dotPositionB);
        rectTransform.anchorMin = new Vector2(0, 0);
        rectTransform.anchorMax = new Vector2(0, 0);
        rectTransform.sizeDelta = new Vector2(distance, 3f);
        rectTransform.anchoredPosition = dotPositionA + dir * distance * .5f;
        rectTransform.localEulerAngles = new Vector3(0, 0, UtilsClass.GetAngleFromVectorFloat(dir));
        return gameObject;
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {

    }
}

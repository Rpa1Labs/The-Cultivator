using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;


public class capteurhumiditésol : MonoBehaviour
{
  
    [SerializeField]
    public Measures measures;

    [SerializeField]
    public string jsonString;

    [SerializeField]
    public Graph graphique;

    [SerializeField]
    Canvas canvas;


    public List<int> moistureList = new List<int>();
    public List<string> dateList = new List<string>();


    private void Awake()
    {
       
    }

    IEnumerator GetText()
    {
        UnityWebRequest uwr = UnityWebRequest.Get("http://54.36.191.243:5000/HumiditySoil");
        yield return uwr.SendWebRequest();
        Debug.Log(uwr.downloadHandler.text);
        jsonString = uwr.downloadHandler.text;
         measures = JsonUtility.FromJson<Measures>(jsonString);
        yield return measures;
       


    }

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GetText());
 
    }
    public void TaskOnClick()
    {
        
        StartCoroutine(GetText());
        canvas.GetComponent<Canvas>();
        for (int i = 0  /*measures.measures.Length - 3*/; i < measures.measures.Length; i++)
        {
            moistureList.Add((int)measures.measures[i].Soil_moisture);
            dateList.Add(measures.measures[i].time);
        }
        canvas.gameObject.SetActive(true);
        graphique = GameObject.FindObjectOfType(typeof(Graph)) as Graph;
        graphique.ShowGraph(moistureList, dateList);
        moistureList.Clear();
        dateList.Clear();
    }

    // Update is called once per frame
    void Update()
    {


    }
 
    public void taskclickclose()
    {
        
        canvas.gameObject.SetActive(false);
  

    }

   /* private void OnTriggerEnter(Collider other)
    {
        StartCoroutine(GetText());
        canvas.GetComponent<Canvas>();
        canvas.gameObject.SetActive(true);
        for (int i = 0 ; i < measures.measures.Length; i++)
        {
            moistureList.Add(measures.measures[i].fields.moisture);
            dateList.Add(measures.measures[i].time);
        }
        graphique = GameObject.FindObjectOfType(typeof(Graph)) as Graph;
        graphique.ShowGraph(moistureList, dateList);
    }*/
}


[System.Serializable]
public class Measure
{
    public string time;
    public float Soil_moisture;
}


[System.Serializable]
public class Measures
{
    public Measure[] measures;
}
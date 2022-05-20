using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class CapteurHATA : MonoBehaviour
{
    [SerializeField]
    public Measures measuresTA;
    [SerializeField]
    public Measures measuresHA;

    [SerializeField]
    public string jsonStringTA;
    [SerializeField]
    public string jsonStringHA;

    [SerializeField]
    public Graph graphique;

    [SerializeField]
    Canvas canvas;


    public List<int> airtemperatureList = new List<int>();
    public List<int> airhumidityList = new List<int>();
    public List<string> dateList = new List<string>();
    IEnumerator GetText()
    {
        UnityWebRequest uwr = UnityWebRequest.Get("http://54.36.191.243:5000/HumidityAir");
        yield return uwr.SendWebRequest();
        Debug.Log(uwr.downloadHandler.text);
        jsonStringHA = uwr.downloadHandler.text;
        measuresHA= JsonUtility.FromJson<Measures>(jsonStringHA);
        yield return measuresHA;
        UnityWebRequest uwr2 = UnityWebRequest.Get("http://54.36.191.243:5000/TemperatureAir");
        yield return uwr2.SendWebRequest();
        Debug.Log(uwr2.downloadHandler.text);
        jsonStringTA = uwr2.downloadHandler.text;
        measuresTA = JsonUtility.FromJson<Measures>(jsonStringTA);
        yield return measuresHA;


    }

    public void TaskOnClickHA()
    {
       
        StartCoroutine(GetText());
        canvas.GetComponent<Canvas>();
        for (int i = 0  /*measures.measures.Length - 3*/; i < measuresHA.measures.Length; i++)
        {
            airhumidityList.Add((int)measuresHA.measures[i].Air_Humidity);
            dateList.Add(measuresHA.measures[i].time);
        }
        canvas.gameObject.SetActive(true);
        graphique = GameObject.FindObjectOfType(typeof(Graph)) as Graph;
        graphique.ShowGraph(airhumidityList, dateList);
        airhumidityList.Clear();
        dateList.Clear();
    }
    public void taskclickcloseHA()
    {
        canvas.gameObject.SetActive(false);
    }

    public void TaskOnClickTA()
    {
        StartCoroutine(GetText());
        canvas.GetComponent<Canvas>();
        for (int i = 0  /*measures.measures.Length - 3*/; i < measuresTA.measures.Length; i++)
        {
            airtemperatureList.Add((int)measuresTA.measures[i].Temperature_Air);
            dateList.Add(measuresTA.measures[i].time);
        }
        canvas.gameObject.SetActive(true);
        graphique = GameObject.FindObjectOfType(typeof(Graph)) as Graph;
        graphique.ShowGraph(airtemperatureList, dateList);
        airtemperatureList.Clear();
        dateList.Clear();
    }
    public void taskclickcloseTA()
    {
        canvas.gameObject.SetActive(false);
    }

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GetText());

    }

    // Update is called once per frame
    void Update()
    {
        
    }


    [System.Serializable]
    public class Measure
    {
        public string time;
        public float Air_Humidity;
        public float Temperature_Air;
    }


    [System.Serializable]
    public class Measures
    {
        public Measure[] measures;
    }

}

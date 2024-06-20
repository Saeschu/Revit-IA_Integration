# Integration von IDS und bSDD in Revit

Die Informationsanforderung betreffend eines Informationsbestellenden und Lieferzeitpunktes wird anschliessend in die Autorenapplikation importiert, um diese entsprechen zu konfigurieren und die enthaltenen Attribute und Properties auf die der Autorenapplikation zu überführen. Während der Modellierung erfolgt die automatisierte Validierung der alphanumerischen Informationseingabe mittels der importierten Informationsanforderungen. Die Bereitstellung der Informationen erfolgt für die geforderte Teilmenge der Informationsanforderung in dem Austauschformat des Industry Foundation Classes (IFC) -Schemas. Die Informationsbereitstellung wird beim Export aus der Autorenapplikation mittels der Informationsanforderung validiert. Die Einbindung des Service bSDD in den Informationsaustausch ermöglicht die Veröffentlichung und Abfragen von Klassifikationen, Autorenapplikation und zukünftig die Nutzung der Mehrsprachigkeit des IFC-Schemas. Darüber hinaus können auf bSDD, Klassifikationen über Properties und Assoziationen des IFC-Schemas formal beschrieben werden. Durch die formal beschriebenen Klassifikationen in Kombination mit der Informationsanforderung in IDS ist die teilautomatisierte Anreicherung von Objekten mit diesen Informationen in der Autorenapplikation möglich.

# Informationsbereitstellung mit Revit 
Die Integration von IDS und bSDD in Revit basiert auf dem Revit AddIn Pyrevit (https://github.com/pyrevitlabs). Die Umsetzung erfolgt aus einer Kombination von IronPython und CPython. Die Anwendung der im Umfang eines Proof of Concept (PoC) entwickelten Integration zeigt sich in der Autorenapplikation wie folgt:

https://github.com/Saeschu/Revit-IA_Integration/assets/33346813/ba8e695f-8145-460a-a1fd-b2458c7fbac6


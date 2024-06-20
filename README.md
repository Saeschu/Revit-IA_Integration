# Integration von IDS und bSDD in Revit
Die Informationsanforderung betreffend eines Informations-bestellenden und Lieferzeitpunktes wird anschliessend in die Autorenapplikation importiert, um diese entsprechen zu Konfigurieren und die enthaltenen Attribute und Properties auf die der Autorenapplikation zu überführen (Fig. 1 Autorenapplikation). Während der Modellierung erfolgt die automatisierte Validierung der alphanumerischen Informationseingabe mittels den importieren Informationsanforderungen. Die Bereitstellung der Informationen erfolgt für die geforderten Teilmenge der Informations-anforderung in dem Austauschformat des Industry Foundation Classes (IFC) -Schemas.
Die Informationsbereitstellung wird beim Export aus der Autorenapplikation mittels der Informationsanforderung validiert.
Die Einbindung des Service bSDD in den Informationsaustausch ermöglicht die Veröffentlichung und Abfragen von Klassifikationen Autorenapplikation und zukünftig die Nutzung der Mehrsprachigkeit des IFC-SChemas. Darüber hinaus können auf bSDD, Klassifikationen über Properties und Assoziationen des IFC-Schemas formal beschreiben werden. Durch die formal beschriebenen Klassifikationen in Kombination mit der Informationsanforderung in IDS ist die teilautomatisierte Anreicherung von Objekten mit diesen Informationen in der Autorenapplikation möglich. 


# Informationsbereitstellung mit Revit
Die Integration von IDS und bSDD in Revit ist basiert auf den Revit AddIn Pyrevit. Die Umsetzung erfolgt aus einer Kombination in IronPython und CPython. 
Die Anwendung der, im Umfang eines Proof of Concept (PoV) entwickelte, Integration zeigt sich in der Autorenapplikation wie folgt:

https://github.com/Saeschu/Revit-IA_Integration/assets/33346813/2f9e720a-6bc2-4d30-8355-acc16eed03bb


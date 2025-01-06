package presto.android.gui.clients.wtg.model;

import java.util.Objects;

import presto.android.gui.graph.NObjectNode;
import presto.android.gui.wtg.EventHandler;

public class Event {

	private String type;
	private String handler;
	private int widgetId;
	private String widgetClass;
	private String widgetName;

	public Event(EventHandler e) {	
		this.type = e.getEvent().toString();
		this.handler = (e.getEventHandler() == null) ? "" : e.getEventHandler().getSignature();
		if (e.getWidget() != null) {
			NObjectNode guiWidget = e.getWidget();
			this.widgetId = guiWidget.id;
			this.widgetClass = guiWidget.getClassType().getName();
			if (guiWidget.idNode != null) {
				this.widgetName = guiWidget.idNode.getIdName();
				this.widgetId = guiWidget.idNode.getIdValue();
			}
		}
	}

	public String getType() {
		return type;
	}

	public String getHandler() {
		return handler;
	}

	public int getWidgetId() {
		return widgetId;
	}

	public String getWidgetClass() {
		return widgetClass;
	}

	public String getWidgetName() {
		return widgetName;
	}

	@Override
	public int hashCode() {
		return Objects.hash(handler, type, widgetClass, widgetId, widgetName);
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if ((obj == null) || (getClass() != obj.getClass()))
			return false;
		Event other = (Event) obj;
		return Objects.equals(handler, other.handler) && Objects.equals(type, other.type) && Objects.equals(widgetClass, other.widgetClass) && widgetId == other.widgetId && Objects.equals(widgetName, other.widgetName);
	}

	@Override
	public String toString() {
		return String.format("Event [type=%s, handler=%s, widgetId=%s, widgetClass=%s, widgetName=%s]", type, handler, widgetId, widgetClass, widgetName);
	}

}

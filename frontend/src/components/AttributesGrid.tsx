import { Attribute } from "../types";

type Props = {
  attributes: Attribute[];
};

export function AttributesGrid({ attributes }: Props) {
  if (attributes.length === 0) {
    return (
      <div className="card empty-state">Характеристики пока не заданы.</div>
    );
  }

  return (
    <div className="card">
      <h2>Характеристики</h2>
      <div className="attributes">
        {attributes.map((attribute) => (
          <div key={attribute.name} className="attribute-item">
            <strong>{attribute.value}</strong>
            <span>{attribute.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

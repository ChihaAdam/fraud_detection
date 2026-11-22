import './NumberField.css'

type Props = {
  id: string
  label: string
  value: string
  onChange: (value: string) => void
  invalid?: boolean
  index?: string
  placeholder?: string
  variant?: 'core' | 'vector'
}

export function NumberField({
  id,
  label,
  value,
  onChange,
  invalid = false,
  index,
  placeholder = '0',
  variant = 'vector',
}: Props) {
  return (
    <div className={`field field-${variant}`}>
      <label htmlFor={id}>
        {label}
        {index && <span>{index}</span>}
      </label>
      <input
        id={id}
        type="number"
        step="any"
        inputMode="decimal"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        aria-invalid={invalid}
        placeholder={placeholder}
      />
    </div>
  )
}

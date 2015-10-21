package bakery

type Session map[string]interface{}

type Provider interface {
	Login() (Session, error)
}
